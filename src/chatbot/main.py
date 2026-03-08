import os
from dotenv import load_dotenv

# Load environment variables FIRST, before any other imports that might depend on them
load_dotenv()
print(f"DEBUG: OPENAI_API_KEY loaded: {bool(os.getenv('OPENAI_API_KEY'))}")

from langchain_core.messages import HumanMessage

from .graph import runnable

def main():
    # Ensure LangSmith tracing is enabled
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if llm_provider not in ["openai", "google"]:
        print(f"Error: Invalid LLM_PROVIDER '{llm_provider}'. Please set LLM_PROVIDER to 'openai' or 'google' in your .env file.")
        return

    if not os.getenv("LANGCHAIN_API_KEY"):
        print("Warning: LANGCHAIN_API_KEY not found. LangSmith tracing might not work.")

    if llm_provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY not found. Please set it in your .env file for OpenAI LLM_PROVIDER.")
            return
    elif llm_provider == "google":
        if not os.getenv("GOOGLE_API_KEY"):
            print("Error: GOOGLE_API_KEY not found. Please set it in your .env file for Google LLM_PROVIDER.")
            return

    if not os.getenv("TAVILY_API_KEY"):
        print("Warning: TAVILY_API_KEY not found. Web search tool might not be available.")

    print("Chatbot started! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting chatbot.")
            break

        # Invoke the LangGraph runnable
        # The input to the runnable is a dictionary with a "messages" key
        # The first message from the user should be a HumanMessage
        response = runnable.invoke({"messages": [HumanMessage(content=user_input)]})

        # The response from the runnable is also a dictionary with a "messages" key
        # The last message in the list is the agent's final answer
        agent_response = response["messages"][-1].content
        print(f"Bot: {agent_response}")

if __name__ == "__main__":
    main()
