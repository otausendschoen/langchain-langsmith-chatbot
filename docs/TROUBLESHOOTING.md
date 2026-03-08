# Troubleshooting Guide

This document provides solutions to common issues encountered during the setup and execution of the chatbot.

## 1. Poetry `No file/folder found for package` Error

**Error Message:**
```
Error: The current project could not be installed: No file/folder found for package langchain-langsmith-chatbot
If you do not want to install the current project use --no-root.
...
```

**Reason:**
Poetry couldn't find the main project package because our project uses a `src` layout (code is in `src/chatbot/`), and Poetry wasn't explicitly told where to look.

**Solution:**
Add the `packages` configuration to your `pyproject.toml` file to point Poetry to the correct source directory.

**Fix:**
Open `pyproject.toml` and add the following line under the `[tool.poetry]` section:

```toml
[tool.poetry]
# ... existing lines ...
packages = [{include = "chatbot", from = "src"}] # Add this line
```

After modifying, run `poetry install` again.

## 2. `ModuleNotFoundError: No module named 'langchain_community'`

**Reason:**
The `langchain_community` package, which contains many specific tools and integrations (like `TavilySearchResults`), needs to be explicitly installed as a separate dependency. Additionally, this often involves updating the core `langchain` and `langgraph` packages to compatible `1.x` versions due to recent architectural changes in the LangChain ecosystem.

**Solution:**
Add `langchain-community` and ensure all related LangChain packages are on compatible `1.x` versions.

**Fix:**
Run the following Poetry command:

```bash
poetry add langchain@latest langgraph@latest langchain-openai@latest langchain-community@latest
```
This command updates `langchain`, `langgraph`, and `langchain-openai` to their latest compatible versions (which should align to `1.x`) and adds `langchain-community`.

## 3. `ImportError: cannot import name 'ToolNode' from 'langgraph.prebuilt'`

**Reason:**
This error often indicates a corrupted virtual environment or an issue where the `langgraph` package isn't correctly installed or accessible, despite `poetry install` reporting success.

**Solution:**
Completely remove and recreate the virtual environment, then reinstall all dependencies.

**Fix:**
1.  **Remove the existing virtual environment:**
    ```bash
    rm -rf .venv
    ```
2.  **Re-install all dependencies into a fresh virtual environment:**
    ```bash
    poetry install
    ```
3.  Then, try running the chatbot again.

## 4. `KeyError: "Input to ChatPromptTemplate is missing variables {'input'}. Expected: ['input'] Received: ['messages']"`

**Reason:**
The `ChatPromptTemplate` in `src/chatbot/graph.py` was expecting a single `input` variable, but the agent was passing a list of `messages` from the `AgentState`. This was a mismatch in how the prompt was defined and how the state was provided.

**Solution:**
Modify the `ChatPromptTemplate` to use `MessagesPlaceholder` to correctly accept the list of messages from the agent's state.

**Fix:**
Open `src/chatbot/graph.py` and modify the prompt definition:

**Original (incorrect) prompt definition:**
```python
from langchain_core.prompts import ChatPromptTemplate

# ...

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's request only based on the given context."),
        ("human", "{input}"),
    ]
)
```

**New (correct) prompt definition:**
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # Add MessagesPlaceholder

# ...

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's request only based on the given context."),
        MessagesPlaceholder(variable_name="messages") # Use MessagesPlaceholder
    ]
)
```

## 5. `TypeError: can only concatenate list (not "AIMessage") to list`

**Reason:**
The `agent_node` function in `src/chatbot/graph.py` was returning a single `AIMessage` object from the LLM, but LangGraph's state update mechanism (specifically `operator.add` for the `messages` list) expected a *list* of messages to concatenate.

**Solution:**
Ensure the `agent_node` always returns a list of messages under the `messages` key, even if it's a list containing a single new message.

**Fix:**
Open `src/chatbot/graph.py` and modify the `agent_node` function's return statement:

**Original (incorrect) return:**
```python
def agent_node(state: AgentState):
    # ...
    result = agent.invoke(state)
    return {"messages": result} # <-- THIS LINE
```

**New (correct) return:**
```python
def agent_node(state: AgentState):
    # ...
    result = agent.invoke(state)
    return {"messages": [result]} # <-- WRAP 'result' IN A LIST
```

## 6. `openai.RateLimitError` or `OpenAIError` (`api_key client option must be set...`)

**Reason:**
This means your `OPENAI_API_KEY` is either:
*   Not correctly set in your `.env` file (e.g., missing, typo, or extra quotes/characters).
*   Your OpenAI account has exceeded its usage quota or hit a rate limit.

**Solution:**
1.  **Check `.env`:** Ensure `OPENAI_API_KEY` is set correctly in your `.env` file, without quotes or extra characters.
2.  **Check OpenAI Account:** Verify your OpenAI usage and billing details. Top up your account or generate a new key if necessary.

## 7. LangSmith `403 Client Error: Forbidden` (Authentication failed)

**Reason:**
This occurs when the `LANGCHAIN_API_KEY` you've provided is rejected by the LangSmith server. This is typically due to:
*   An incorrect or expired `LANGCHAIN_API_KEY`.
*   The key not having the necessary permissions for your LangSmith project.
*   **Crucially, a regional mismatch:** If your LangSmith account or project is hosted in a specific region (e.g., EU), you must use the corresponding regional endpoint.

**Solution:**
1.  **Verify `LANGCHAIN_API_KEY`:** Double-check your key in your LangSmith account dashboard. Generate a new one if unsure.
2.  **Set `LANGCHAIN_ENDPOINT` (if regional):** If your LangSmith account is regional, you MUST set the `LANGCHAIN_ENDPOINT` environment variable in your `.env` file.
    *   For West Europe servers, add: `LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com`
    *   (Consult LangSmith documentation for other regions if applicable).

## General Troubleshooting Tip:
If you encounter persistent issues after dependency changes, a full virtual environment recreation (`rm -rf .venv` then `poetry install`) can often resolve underlying environment problems.
