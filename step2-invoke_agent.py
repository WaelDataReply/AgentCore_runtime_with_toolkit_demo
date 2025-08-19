import boto3
import json

# Agent ARN
agent_arn = "arn:aws:bedrock-agentcore:eu-central-1:<account_ID>:runtime/<agent_ID>"

# Initialize Bedrock agent client
agentcore_client = boto3.client(
    'bedrock-agentcore',
    region_name='eu-central-1'
)

boto3_response = agentcore_client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    qualifier="DEFAULT",
    payload=json.dumps({"prompt": "How to invest in crypto?"})
)

print("Response content type:", boto3_response.get("contentType", "No content type"))

if "text/event-stream" in boto3_response.get("contentType", ""):
    content = []
    for line in boto3_response["response"].iter_lines(chunk_size=1):
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                line = line[6:]
                print(line)
                content.append(line)
    
    print("\n".join(content))
else:
    try:
        events = []
        # Afficher la structure de la réponse pour le débogage
        print("Response structure:", type(boto3_response.get("response")))
        
        # Si response est un objet StreamingBody
        if hasattr(boto3_response.get("response"), "read"):
            raw_response = boto3_response["response"].read().decode("utf-8")
            #print("Raw response:--> ", raw_response)
            try:
                parsed_response = json.loads(raw_response)
                print("Parsed response:--> ", parsed_response)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print("Displaying raw response instead:")
                print(raw_response)
        else:
            # Si response est une liste ou un autre type
            for event in boto3_response.get("response", []):
                print("Event type:", type(event))
                events.append(event)
                
            if events:
                try:
                    # Essayer de décoder et parser le premier événement
                    decoded_event = events[0].decode("utf-8")
                    print("Decoded event:", decoded_event)
                    parsed_event = json.loads(decoded_event)
                    print("Parsed event:", parsed_event)
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    print(f"Error processing event: {e}")
                    print("Raw event:", events[0])
    except Exception as e:
        print(f"Error processing response: {e}")
        print("Full response object:", boto3_response)