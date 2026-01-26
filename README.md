# LangChain LangSmith Chatbot

This project is an experimental chatbot built to learn and demonstrate AI engineering skills using the following technologies:

- **Python**
- **LangChain & LangGraph** for building stateful, multi-step conversational agents.
- **LangSmith** for tracing, monitoring, and debugging.
- **OpenAI** for the language model.
- **Poetry** for dependency management.

## Getting Started

1.  **Install dependencies:**
    ```bash
    poetry install
    ```
2.  **Set up environment variables:**
    Create a `.env` file and add your API keys:
    ```
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_API_KEY="..."
    OPENAI_API_KEY="..."
    TAVILY_API_KEY="..."
    ```
3.  **Run the chatbot:**
    ```bash
    poetry run python -m src.chatbot.main
    ```
