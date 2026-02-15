import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from .graph import runnable

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Ensure LangSmith tracing is enabled
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("Warning: LANGCHAIN_API_KEY not found. LangSmith tracing might not work.")
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found. Please set it in your .env file.")
        return
    if not os.getenv("TAVILY_API_KEY"):
        print("Warning: TAVILY_API_KEY not found. Web search tool might not work.")

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
