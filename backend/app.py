import json
import boto3
import base64
import os
from datetime import datetime


s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bucket = os.environ['BUCKET_NAME']
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename')
        content = body.get('content')


        if not filename or not content:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Faltan campos 'filename' o 'content'"})
            }


        # Guardar archivo en S3
        file_bytes = base64.b64decode(content)
        s3.put_object(Bucket=bucket, Key=filename, Body=file_bytes)


        # Guardar metadata en DynamoDB
        table.put_item(Item={
            'filename': filename,
            'uploaded_at': datetime.now().isoformat()
        })


        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Archivo {filename} subido con éxito."
            })
        }


    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
