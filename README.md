# Databricks-API-Self-Service-Layer-AWS

Here are the steps to deploy the following sample setup in your AWS account:



![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/Databricks%20API%20Self%20Service%20Layer.png)

1. Prerequisites: <br />
  1.1 Databricks Workspace is up and running <br />
  1.2 [Generate](https://docs.databricks.com/dev-tools/api/latest/authentication.html#generate-a-personal-access-token) Databricks PAT ( Personal Access Token) <br />
  1.3 [Create ](https://docs.databricks.com/clusters/create.html#create-a-cluster)a simple Databricks cluster with one worker node <br />
  1.4 Make a note of the clusterid of the cluster you created <br />
     Note- Simple way to get the clusterid is to click on your cluster in the Clusters tab, Change the UI interface to json, It will give the all details about your            cluster including the clusterid <br />
     
   ![alt text](https://forums.databricks.com/storage/attachments/1028-clusterid.png) 
           
           
  1.5 Download the AWS CloudFormation Tempate- DatabricksAPIservice.yaml and AWS Lambda Source Code - DatabricksAPIServiceLayer.zip  <br />
  1.6 Upload above artifacts in the s3 bucket under your AWS account <br />
  1.7 Copy workspace URL with https, that will act as host parameter in the CloudFormation script <br />

2. Execute the CloudFomration script to delpoy the sample API self service solution in your AWS account <br />
  2.1 Log on to your AWS account console, go to CloudFormaion service, then click create new stack -> select "with a new resources (Standard) option<br />
  2.2 provide s3 path where you have uploaded above CloudFormation script <br />
  2.3 Provide values for below given parameters: <br />
    - clutserId- provide clusterid copied from above the step <br />
    - host - provide databricks workspace URL without https <br />
    - lambdas3path - provide s3 path of lambda zip archive file <br />
    - language - let the language be sql <br />
    - PAT - provide the above generated Databricks PAT token <br />
    
 3. Click "Next" till you reach "create stack" option, click on the create stack option.
 
 4. Once successful a CloudFormation stack will create below resources-
   - API Gateway 
   - "Select" resource and method attached to that resource 
   - deployment as "test" for the API gateway
   - AWS Lambda Function - testDBAPILambda as an "API Mediation layer 
   - Databricks SQL execuiont context using custom Lambda fucntion
   - A secrte- DBaccesskey in AWS Secret Manager to securly save your Databricks PAT
   
 5. Go to output section of CloudFormation, where in you will find "ApIurl" key which has value making GET api call to newly createed Lambada function by passing the id parameter , Grab that URL and paste it into the broweser and hit enter
 
 ![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/output/CloudFormation_output.png)
 
  once you run the output URL on the browser, it will make a GET api call to Lambda by passing id paramter as 1, then Lambda will in turn parse the GET api      request along with the parameter and handle all the back and forth communication between the Databricks to get the output back (under the hood Lambda will execute the SQL query as "select * from diamons where id = {parameter_passed_by API request}"), once Lambda receives the request it will relay it back to API Gateway, which in turn relay back to client browser as given below 
  
 ![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/output/API_output.png)
 
 
 try changing the id paramter values in browser to 2 or 3 or 4 and hit enter, each time you will get a different output, you have successfully deployed Databricks Self Service API Layer!
 
 
 ![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/output/API_output1.png)
 
 
 
      
  
           
           
    
