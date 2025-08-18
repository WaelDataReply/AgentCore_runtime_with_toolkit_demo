from utils import create_agentcore_role
from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session

agent_name="strands_claude"
agentcore_iam_role = create_agentcore_role(agent_name=agent_name)


boto_session = Session(region_name='eu-central-1')
region = boto_session.region_name
print("region--->", region)

agentcore_runtime = Runtime()

response = agentcore_runtime.configure(
    entrypoint="agent.py",
    execution_role=agentcore_iam_role['Role']['Arn'],
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    region=region,
    agent_name=agent_name+"3"
)
print ("response--->", response)

launch_result = agentcore_runtime.launch()
print("launch_result--->", launch_result)