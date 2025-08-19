from strands import Agent, tool
from strands_tools import calculator, python_repl, shell, http_request, editor, file_write
from strands.models import BedrockModel

# ---------------------------
# Specialized Assistants
# ---------------------------

model_id = "eu.anthropic.claude-3-5-sonnet-20240620-v1:0"
model = BedrockModel(
    model_id=model_id, region_name='eu-central-1'
)

FINANCE_ASSISTANT_SYSTEM_PROMPT = (
    "You are a finance expert who answers questions about banking products, "
    "investments, and financial analyses. Use the calculator when necessary."
)

@tool
def finance_assistant(query: str) -> str:
    """Process and respond to finance-related queries."""
    formatted_query = f"Please answer this financial question with detailed analysis: {query}"
    finance_agent = Agent(
        model=model,
        system_prompt=FINANCE_ASSISTANT_SYSTEM_PROMPT,
        tools=[calculator],
    )
    return str(finance_agent(formatted_query))


LEGAL_ASSISTANT_SYSTEM_PROMPT = (
    "You are a legal expert who answers questions about banking regulations, "
    "contract law, and compliance. Use online sources when necessary."
)

@tool
def legal_assistant(query: str) -> str:
    """Respond to legal and regulatory questions."""
    formatted_query = f"Analyze this legal question: {query}"
    legal_agent = Agent(
        model=model,
        system_prompt=LEGAL_ASSISTANT_SYSTEM_PROMPT,
        tools=[http_request],
    )
    return str(legal_agent(formatted_query))


WRITING_ASSISTANT_SYSTEM_PROMPT = (
    "You assist in drafting and improving professional documents, "
    "emails, and banking communications."
)

@tool
def writing_assistant(query: str) -> str:
    """Help with drafting and editing documents."""
    formatted_query = f"Help draft or improve this document: {query}"
    writing_agent = Agent(
        model=model,
        system_prompt=WRITING_ASSISTANT_SYSTEM_PROMPT,
        tools=[editor, file_write],
    )
    return str(writing_agent(formatted_query))


TECHNICAL_ASSISTANT_SYSTEM_PROMPT = (
    "You are a technical expert who answers questions about computer systems, "
    "data security, and can write, run, and explain code."
)

@tool
def technical_assistant(query: str) -> str:
    """Answer technical and IT questions."""
    formatted_query = f"Answer this technical question, write and run code if needed: {query}"
    technical_agent = Agent(
        model=model,
        system_prompt=TECHNICAL_ASSISTANT_SYSTEM_PROMPT,
        tools=[python_repl, shell, file_write],
    )
    return str(technical_agent(formatted_query))


GENERAL_ASSISTANT_PROMPT = (
    "You answer general questions that don't fall under a specific domain."
)
@tool
def general_assistant(query: str) -> str:
    """Assistant for general questions."""
    gen_agent = Agent(
        model=model,
        system_prompt=GENERAL_ASSISTANT_PROMPT,
        tools=[],
    )
    return str(gen_agent(query))


# ---------------------------
# Orchestrator (Main Agent)
# ---------------------------

MAIN_SYSTEM_PROMPT = (
    "You are an orchestrator that receives user questions and "
    "routes them to the most appropriate expert assistant: finance_assistant, legal_assistant, "
    "writing_assistant, technical_assistant, or general_assistant. "
    "Return only the specialist's answer."
)

main_agent = Agent(
    model=model,
    system_prompt=MAIN_SYSTEM_PROMPT,
    tools=[
        finance_assistant,
        legal_assistant,
        writing_assistant,
        technical_assistant,
        general_assistant,
    ],
)


# ---------------------------
# Command Line Interface
# ---------------------------

def main():
    print("Credit Agricole Multi-Agent Demo")
    print("Type 'exit' to quit.\n")
    while True:
        user_input = input("Ask your question: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        try:
            response = main_agent(user_input)
            print(f"\nResponse:\n{response}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()