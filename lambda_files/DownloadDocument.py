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