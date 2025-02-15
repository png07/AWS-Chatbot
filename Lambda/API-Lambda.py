import json
import boto3
import uuid

# Initialize Bedrock Agent Runtime Client
bedrock_agent = boto3.client(service_name="bedrock-agent-runtime", region_name="us-east-1")

# Replace with your actual Bedrock Agent & Alias IDs
BEDROCK_AGENT_ID = "781WPOXLXW"
BEDROCK_AGENT_ALIAS_ID = "OOBNJA6FWJ"

def invoke_bedrock_agent(user_query, session_id):
    """Calls Bedrock Agent and handles streaming response properly."""
    response_stream = bedrock_agent.invoke_agent(
        agentId=BEDROCK_AGENT_ID,
        agentAliasId=BEDROCK_AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=user_query
    )

    # ✅ Extract text response from event stream
    result_text = ""
    for event in response_stream["completion"]:  # Stream response handling
        if "chunk" in event:
            result_text += event["chunk"]["bytes"].decode("utf-8")

    return result_text

def lambda_handler(event, context):
    """AWS Lambda function handler to process API requests."""
    try:
        if "body" in event:  # API Gateway case
            body = json.loads(event["body"])
        else:  # Direct Lambda invocation case
            body = event

        user_query = body.get("query")
        if not user_query:
            return {"statusCode": 400, "body": json.dumps({"error": "No query provided"})}

        # Generate a unique session ID if not provided
        session_id = body.get("sessionId", str(uuid.uuid4()))

        # Call Bedrock Agent and process response
        agent_response = invoke_bedrock_agent(user_query, session_id)

        return {"statusCode": 200, "body": json.dumps({"response": agent_response})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
