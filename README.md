# Databricks-API-Self-Service-Layer-AWS

Solution Brief:

The objective of this sample setup is to give you end-to-end visibility into how the Databricks API self-service layer solution will work.

Once you deploy this solution in your AWS account, you can use it to make a GET API call by passing a parameter named "id" and then under the hood, the API layer will query the sample dataset via Databrick cluster to table name "diamonds" by executing the query as "select * from diamonds where id= {parameter_passed_by API request}" and then the send output back to the client via API response


![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/Databricks%20API%20Self%20Service%20Layer.png)


Here are the steps to deploy the sample set up in your AWS account

1. Prerequisites: <br />
  1.1 Databricks Workspace is up and running <br />
  1.2 [Generate](https://docs.databricks.com/dev-tools/api/latest/authentication.html#generate-a-personal-access-token) Databricks PAT ( Personal Access Token) <br />
  1.3 [Create ](https://docs.databricks.com/clusters/create.html#create-a-cluster)a simple Databricks cluster with one worker node <br />
  1.4 Make a note of the clusterid of the cluster you created <br />
     Note- Simple way to get the clusterid is to click on your cluster in the Clusters tab, Change the UI interface to JSON, It will give all details about your  cluster including the clusterid <br />
     
   ![alt text](https://forums.databricks.com/storage/attachments/1028-clusterid.png) 
           
           
  1.5 Download the AWS CloudFormation Template- DatabricksAPIservice.yaml and AWS Lambda Source Code - DatabricksAPIServiceLayer.zip  <br />
  1.6 Upload the above artifacts in the s3 bucket under your AWS account <br />
  1.7 Copy workspace URL without HTTPS, that will act as host parameter in the CloudFormation script <br />

2. Execute the CloudFomration script to deploy the sample API self-service solution in your AWS account <br />
  2.1 Log on to your AWS account console, go to CloudFormaion service, then click create new stack -> select "with a new resources (Standard) option<br />
  2.2 provide s3 path where you have uploaded the above CloudFormation script <br />
  2.3 Provide values for below given parameters: <br />
    - clutserId- provide clusterid copied from above the step <br />
    - host - provide Databricks workspace URL without HTTPS <br />
    - lambdas3path - provide s3 path of lambda zip archive file <br />
    - language - let the language be sql <br />
    - PAT - provide the above generated Databricks PAT token <br />
    
 3. Click "Next" till you reach the "create stack" step, click on the create stack option.
 
 4. Once successful a CloudFormation stack will create the below resources-
   - API Gateway 
   - "Select" resource and method attached to that resource 
   - deployment as "test" for the API gateway
   - AWS Lambda Function - testDBAPILambda as an "API Mediation layer 
   - Databricks SQL execution context using custom Lambda function
   - A secret- DBaccesskey in AWS Secret Manager to securely save your Databricks PAT
   
 5. Go to the output section of CloudFormation, wherein you will find the "ApIurl" key which has value making GET API call to newly created Lambda function by passing the id parameter, Grab that URL and paste it into the browser and hit enter
 
 ![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/output/CloudFormation_output.png)
 
  once you run the output URL on the browser, it will make a GET API call to Lambda by passing id parameter as 1, then Lambda will, in turn, parse the GET API request along with the parameter and handle all the back and forth communication between the Databricks to get the output back (under the hood Lambda will execute the SQL query as "select * from diamonds where id = {parameter_passed_by API request}"), once Lambda receives the request it will relay it back to API Gateway, which in turn relay back to the client browser as given below 
  
 ![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/output/API_output.png)
 
 
 try changing the id parameter values in the browser to 2 or 3 or 4 and hit enter, each time you will get a different output, you have successfully deployed Databricks Self Service API Layer!
 
 
 ![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/output/API_output1.png)
 
 
 
      
  
           
           
    


