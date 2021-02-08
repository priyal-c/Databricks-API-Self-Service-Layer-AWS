# Databricks-API-Self-Service-Layer-AWS

Here are the steps to deploy the following sample setup in your AWS account:



![alt text](https://github.com/priyal-c/Databricks-API-Self-Service-Layer-AWS/blob/main/Databricks%20API%20Self%20Service%20Layer.png)

1. Prerequisites: <br />
  1.1 Databricks Workspace is up and running <br />
  1.2 Generate Databricks PAT ( Personal Access Token)- [document link](https://docs.databricks.com/dev-tools/api/latest/authentication.html#generate-a-personal-    access-token) <br />
  1.3 [Create ](https://docs.databricks.com/clusters/create.html#create-a-cluster)a simple Databricks cluster with one worker node <br />
  1.4 Make a note of the clusterid of the cluster you created <br />
     Note- Simple way to get the clusterid is to click on your cluster in the Clusters tab, Change the UI interface to json, It will give the all details about your            cluster including the clusterid <br />
           ![alt text](https://forums.databricks.com/storage/attachments/1028-clusterid.png) < br />
  1.5 Download the AWS CloudFormation Tempate- DatabricksAPIservice.yaml and AWS Lambda Source Code - DatabricksAPIServiceLayer.zip <br />
  1.6 Upload above artifacts in the s3 bucket under your AWS account < br />
  1.7 Copy workspace URL with https, that will act as host parameter in the CloudFormation script < br />

2. Execute the CloudFomration script to delpoy the sample API self service solution in your AWS account < br />
  2.1 Log on to your AWS account console, go to CloudFormaion service, then click create new stack -> select "with a new resources (Standard) option< br />
  2.2 provide s3 path where you have uploaded above CloudFormation script < br />
  2.3 Provide values for below given parameters: < br />
      2.3.1 clutserId- provide clusterid copied from above the step < br />
      2.3.2 host - provide databricks workspace URL without https < br />
      2.3.3 lambdas3path - provide s3 path of lambda zip archive file < br />
      2.3.4 language - let the language be sql < br />
      2.3.5 PAT - provide the above generated Databricks PAT token < br />
      
  
           
           
    
