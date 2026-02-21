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
    Create a `.env` file in the project root and add your API keys.
    *   **`OPENAI_API_KEY`**: Your API key for OpenAI. (Required for chatbot function)
    *   **`TAVILY_API_KEY`**: Your API key for Tavily. (Optional; required for web search functionality)
    *   **`LANGCHAIN_API_KEY`**: Your API key for LangSmith. (Optional; required for LangSmith tracing)
    *   **`LANGCHAIN_TRACING_V2`**: Set to `true` to enable LangSmith tracing.
    *   **`LANGCHAIN_ENDPOINT`**: (Optional) The API endpoint for LangSmith. Only required if your LangSmith account is in a specific region (e.g., `https://eu.api.smith.langchain.com` for West Europe).

    Your `.env` file should look like this (replace `...` with your actual keys):
    ```
    OPENAI_API_KEY=sk-...
    TAVILY_API_KEY=tvly-... # Optional
    LANGCHAIN_API_KEY=ls__... # Optional
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com # Only if needed for your region
    ```
    For troubleshooting API key issues, refer to the [Troubleshooting Guide](docs/TROUBLESHOOTING.md).
3.  **Run the chatbot:**
    ```bash
    poetry run python -m src.chatbot.main
    ```
