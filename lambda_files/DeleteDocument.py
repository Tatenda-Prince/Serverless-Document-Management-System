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