# Serverless-Document-Management-System

"Cloud Vault"

# Technical Architecture

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/9cc35fb344b606b4cf30cbb6f6da183b8d62406a/img/Screenshot%202025-02-11%20165509.png)

## Project Overview

The Cloud-Based Document Management System leverages AWS serverless services to enable secure document storage, retrieval, and management. Amazon S3 stores the documents, while DynamoDB maintains metadata such as filenames, timestamps, and user details. AWS Lambda (Python) powers backend logic to handle file operations, with API Gateway exposing RESTful APIs for uploading, downloading, and deleting files. IAM policies ensure secure access control to S3 and DynamoDB. The system will be tested using Postman to validate API functionality, ensuring seamless document management in a scalable and cost-effective cloud environment.


## Features

1.Users can upload files (PDFs, images, docs) to Amazon S3 via API.

2.Stores metadata (filename, timestamp, user ID) in Amazon DynamoDB.

3.Returns a unique S3 file URL for access.

4.Users can request a pre-signed URL to download documents securely.

5.Only authorized users can retrieve files.

6.Users can delete a file via API.

7.The system removes both the file from S3 and its metadata from DynamoDB.

## Prerequisites

1.AWS Account with an IAM User

2.Basic knowledge of the Python Programming Language

## Use Case 

You work at Up the Chelsea Corp as the Cloud Engineer for the company you are tasked with securing storage for employee records, payroll documents, and contracts.
Access control ensures only HR personnel can retrieve sensitive documents for The Humana Resource (HR) Department.


## Step 1: Set Up the S3 Bucket

1.1.Go to the AWS Management Console > S3 > Create bucket.

1.2.Name your bucket (for example document-management-system).

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/d3bef7be1e50c1283118c90b906a849c31a26dd1/img/Screenshot%202025-02-11%20150924.png)

1.3.Enable Versioning (optional but recommended for document management).

Keep other settings as default.


1.3.Once our bucket is successfully created we need to edit our bucket policy


1.2.Create a Bucket Policy:

Attach the following bucket policy to allow access to your Lambda functions:

```language
json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE_NAME"
      },
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::document-management-system/*"
    }
  ]
}

```

Now Replace `YOUR_ACCOUNT_ID` and `YOUR_LAMBDA_ROLE_NAME` with your AWS account ID and the IAM role name used by your Lambda function.


## Step 2: Set Up DynamoDB for Metadata

2.1.In the AWS Management Console navigate to DynamoBD

2.2.Create a DynamoDB Table:

2.3.Go to DynamoDB > Create table.

Name the table DocumentMetadata.

We set the Primary Key as DocumentID (String).

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/4eb121799732329d641c6e0b1a5974fabdd3115d/img/Screenshot%202025-02-11%20151424.png)

Keep other settings as default

2.4.Our Table is successfully created

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/ebab46b05416b316b8a7563bfda9629e2e1ef1c7/img/Screenshot%202025-02-11%20151458.png)



## Step 3: Lets create Lambda Functions

3.1.We’ll create three Lambda functions for Upload, Download, and Delete operations.

3.2.In the AWS Management Console, head to the AWS Lambda dashboard.

3.3.Function Name: UploadDocument

Runtime: Python 3.x

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/e5efda80205d6e841ad03f9881b328e81fec4546/img/Screenshot%202025-02-11%20151607.png)

3.4.In the Management Console, head to the IAM dashboard and click on policy and create a policy.

copy this policy below

```language

json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::your-s3-bucket-name/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:DeleteItem",
                "dynamodb:Scan"
            ],
            "Resource": "arn:aws:dynamodb:your-region:your-account-id:table/your-dynamodb-table-name"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:your-region:your-account-id:log-group:/aws/lambda/your-lambda-function-name:*"
        }
    ]
}

```

3.5.Create a lambda role and attach your custom policy give it name.


3.6.Head back to the Lambda’s “Create function” window. Refresh the existing roles, select the role previously created, then click “Create Function”.

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/e8ba2704f99c3a0cdaf472838fcbf762d84e1fdd/img/Screenshot%202025-02-11%20151629.png)


## Step 4 : Write the Lambda Function Code

4.1.Function Name: `UploadDocument`

Replace the default code with the following Python script:

```python
import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DocumentMetadata')

def lambda_handler(event, context):
    # Parse the file and metadata from the request
    file_content = event['body']
    file_name = event['headers']['file-name']
    file_size = event['headers']['file-size']
    
    # Generate a unique document ID
    document_id = str(uuid.uuid4())
    
    # Upload the file to S3
    s3.put_object(
        Bucket='tatenda-document-management-system',
        Key=document_id,
        Body=file_content
    )
    
    # Save metadata in DynamoDB
    table.put_item(Item={
        'DocumentID': document_id,
        'FileName': file_name,
        'FileSize': file_size,
        'UploadDate': datetime.now().isoformat()
    })
    
    return {
        'statusCode': 200,
        'body': json.dumps({'DocumentID': document_id})
    }
```


4.2.Create another lambda function Download Document

Function Name: `DownloadDocument`

Replace the default code with the following Python script:

```python

import json
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DocumentMetadata')

def lambda_handler(event, context):
    # Get the document ID from the request
    document_id = event['queryStringParameters']['DocumentID']
    
    # Retrieve the file from S3
    file_object = s3.get_object(
        Bucket='tatenda-document-management-system',
        Key=document_id
    )
    file_content = file_object['Body'].read()
    
    # Retrieve metadata from DynamoDB
    metadata = table.get_item(Key={'DocumentID': document_id})['Item']
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': f'attachment; filename="{metadata["FileName"]}"'
        },
        'body': file_content,
        'isBase64Encoded': True
    }
```


4.3.Create another lambda function Delete Document

Function Name: `DeleteDocument`

```python
import json
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DocumentMetadata')

def lambda_handler(event, context):
    # Get the document ID from the request
    document_id = event['queryStringParameters']['DocumentID']
    
    # Delete the file from S3
    s3.delete_object(
        Bucket='tatenda-document-management-system',
        Key=document_id
    )
    
    # Delete metadata from DynamoDB
    table.delete_item(Key={'DocumentID': document_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Document deleted successfully'})
    }

```

## Step 5: lets Set Up API Gateway

5.1.In the AWS Management Console, head to the AWS API Gateway dashboard.

5.2.Create a REST API:

Go to API Gateway > Create API > REST API.

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/cec3a20e4fb49bd765e61cb3ad240ef97cc55ff5/img/Screenshot%202025-02-11%20152622.png)


Name your API ( for example DocumentManagementAPI).


![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/b5565c4edc89334256c6eb0414355339dbe7fdd3/img/Screenshot%202025-02-11%20152648.png)


5.3.Create Resources and Methods:

Create a resource (e.g., /documents).

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/c265e858fe43248f4794a8d1c291ea6eeae2be77/img/Screenshot%202025-02-11%20152742.png)


5.4.Add the following methods:

POST (for uploading documents).


![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/cad99c500e0ccec012d731c3fac46c41592f189a/img/Screenshot%202025-02-11%20152844.png)



GET (for downloading documents).


![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/c43a7a7956e5d994d752d886244dfcb5914f44f5/img/Screenshot%202025-02-11%20152937.png)


DELETE (for deleting documents).

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/3d3a2f2e86c2f46782df3f45f0c51797b10b56bd/img/Screenshot%202025-02-11%20153033.png)

5.5.Deploy the API:

Deploy the API to a stage (e.g., prod).


## Step 6: Test the System Using Postman

1.lets Upload a Document

Method: `POST`

URL: `https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com/prod/documents`

Headers:

`file-name: example.txt`

`file-size: 1024`

Body: Attach the file as binary data.

Click Send

Now lets verify if the our documents metadata were successfully uploaded 

![image_alt](https://github.com/Tatenda-Prince/Serverless-Document-Management-System/blob/5590312f0939fb9688603ac44a54a7d5f9f08f6e/img/Screenshot%202025-02-11%20183259.png)


Check  your DynamoDB if the metadata was saved 

![image_alt]()


check your Amazon if the documenta were successfully saved

![image_alt]()












































