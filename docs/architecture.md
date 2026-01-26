# Chatbot Architecture

This document outlines the architecture for our experimental chatbot.

### Core Technologies

*   **LangChain & LangGraph**: Used to build the core agent logic as a stateful graph.
*   **LangSmith**: Used for observability, tracing, and debugging.
*   **OpenAI**: The provider for the core language model.
*   **Tavily**: The provider for the web search tool.
*   **Poetry**: Used for dependency management.

### Project Structure

The chatbot's code will be organized within the `src/chatbot/` directory.

1.  **Configuration (`.env`)**
    *   A `.env` file in the root directory will be used to securely manage API keys for services like OpenAI, LangSmith, and Tavily.
    *   This file should not be committed to Git.

2.  **State (`src/chatbot/state.py`)**
    *   Defines the "state" of our graph. This is the central data structure that gets passed between nodes.
    *   It will primarily contain the list of messages (`List[BaseMessage]`) to represent the conversation history.

3.  **Tools (`src/chatbot/tools.py`)**
    *   This module will define the tools that the agent can use.
    *   We will start by implementing a single tool: a web search using the Tavily API. This gives the agent the ability to find information online.

4.  **Graph (`src/chatbot/graph.py`)**
    *   This is the heart of the application, where the conversational flow is defined using LangGraph.
    *   **Workflow**: A `StatefulGraph` will be created.
    *   **Nodes**:
        *   `agent`: The "brain" of the chatbot. It is a LangChain agent that, given the conversation state, decides to either respond directly or use a tool.
        *   `action`: The "tool executor". This node runs the tool chosen by the `agent` node and returns the output.
    *   **Edges**:
        *   **Conditional Edging**: Logic will be added to the graph to route the flow based on the `agent`'s output. If the agent decided to use a tool, the graph transitions to the `action` node. If not, the graph finishes the turn.
    *   The compiled graph will be a runnable object that manages the agent's execution cycle.

5.  **Main Entrypoint (`src/chatbot/main.py`)**
    *   This will be the main script to run the chatbot.
    *   It will be responsible for:
        *   Loading environment variables from `.env`.
        *   Setting up LangSmith tracing.
        *   Instantiating and compiling the graph from `graph.py`.
        *   Running an interactive command-line loop that takes user input, invokes the graph, and prints the agent's response.
