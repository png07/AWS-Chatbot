import boto3
import os
import json

bedrock_agent = boto3.client('bedrock-agent')

def lambda_handler(event, context):
    try:
        # Debug print
        print("Environment Variables:", json.dumps(dict(os.environ), indent=2))

        # Get environment variables
        knowledge_base_id = '1ANKHSJYDW'
        data_source_id = 'O1WDETVZYD'

        # Ensure values are not None
        if not knowledge_base_id or not data_source_id:
            raise ValueError("KNOWLEDGE_BASE_ID or DATA_SOURCE_ID is missing in environment variables")

        # Start the ingestion job
        response = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
            clientToken=context.aws_request_id
        )

        print(f"Ingestion job started: {json.dumps(response, default=str)}")
        return {
            'statusCode': 200,
            'body': json.dumps('Ingestion job started successfully')
        }
    except Exception as e:
        print(f"Error starting ingestion job: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
