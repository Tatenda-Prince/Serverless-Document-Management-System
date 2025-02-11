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

![image_alt]()



## Step 3: Lets write Lambda Functions

3.1.We’ll create three Lambda functions for Upload, Download, and Delete operations.








