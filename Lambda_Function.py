import logging
import requests
import json
import time
import boto3
import base64
import os
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# function to reteirve Databricks PAT from AWS Secrets Manager 
def get_secret():

    secret_name = "DBaccesskey"
    region_name = os.environ['AWS_REGION']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            j=json.loads(secret)
            accesskey=j['token']
            return accesskey#json.dumps(accesskey)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            j=json.loads(decoded_binary_secret)
            accesskey=j['token']
            return accesskey#json.dumps(accesskey)

#main lambada handler calling Databricks RESTful APIs
def lambda_handler(event, context):
    logger.info('Python HTTP trigger function processed a request.')
    language_in=os.environ['language']
    clusterId_in= os.environ['clusterId']
    contextId_in=os.environ['contextId']
    host_in=os.environ['host']
    diamond_id= event["queryStringParameters"]["id"] #'1'
    auth_token= get_secret() #call secrets manager function to reterive Daatabricks PAT 
    hed = {'Authorization': 'Bearer ' + auth_token}
    sql_query = "SELECT * from diamonds where _c0= " + json.dumps(diamond_id) #build sql query using parameter passed
    data = {"language": language_in, "clusterId": clusterId_in, "contextId": contextId_in, "command": sql_query}
    url = f"https://{host_in}/api/1.2/commands/execute"
    response = requests.post(url, json=data, headers=hed) #submitt command via POST API
    responsejson = response.json() # capture the response of command submit API
    logger.info('command submitted to Databricks')
    if response.status_code==200:  # command submission successful
        get_url=f"https://{host_in}/api/1.2/commands/status?clusterId={clusterId_in}&contextId={contextId_in}&commandId={responsejson['id']}"
        res_output= requests.get(get_url, headers=hed) # get API to check the status of the command submitted
        res_output_json = res_output.json() 
        status= res_output_json["status"] #update the status variable with the latest status
        
        if status=="Running": # continue to check the status of the command till the command is in the "Running" status
            while status=="Running":
                res_output= requests.get(get_url, headers=hed) # get API to check the status of the command
                res_output_json = res_output.json() 
                status= res_output_json["status"] #update the status variable with the latest status
                time.sleep(2) # add delay in the get API to aviod flood of API request    
        
        # status is in "Queued" state
        if status=="Queued":
             while status=="Queued": # continue to check the status of the command till the command is in the "Queued" status
                res_output= requests.get(get_url, headers=hed) # get API to check the status of the command
                res_output_json = res_output.json() 
                status= res_output_json["status"] #update the status variable with the latest status
                time.sleep(2) # add delay in the get API to aviod flood of API request

         #command execution is Finished
        if  status=="Finished": # once the command is completed, check the type of result
            if res_output_json["results"]["resultType"]== "table": #command was successful and result came back in the table form, return the output
                return {"body":json.dumps(res_output_json["results"]["data"])} #return the results back
            elif res_output_json["results"]["resultType"]== "error":  # command was unsuccessful and return error message
                return {"body": json.dumps(res_output_json["results"]["summary"])} 
    
    elif response.status_code==500:  #serevr side error
         return {"body":json.dumps(responsejson["error"])}    #return the error message
    