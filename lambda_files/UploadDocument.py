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