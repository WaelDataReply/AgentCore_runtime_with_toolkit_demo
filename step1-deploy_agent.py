from utils import create_agentcore_role
from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session

agent_name="finance_multi_agents_system"
## To create a new role
#agentcore_iam_role = create_agentcore_role(agent_name=agent_name)
#print("role --->", agentcore_iam_role['Role']['Arn'])


boto_session = Session(region_name='eu-central-1')
region = boto_session.region_name
print("region--->", region)

agentcore_runtime = Runtime()

response = agentcore_runtime.configure(
    entrypoint="finance_agents_agentcore.py",
    #execution_role=agentcore_iam_role['Role']['Arn'],
    execution_role="arn:aws:iam::<account_ID>:role/agentcore-finance_multi_agents_system-role",
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    region=region,
    agent_name=agent_name+"1"
)
print ("response--->", response)

launch_result = agentcore_runtime.launch()
print("launch_result--->", launch_result)