import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .state import AgentState
from .tools import tools

# 1. Define the Agent
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", (
            "You are a helpful assistant. Respond to the user's request based on the context provided, "
            "especially using information from tool outputs. If a tool output is available, prioritize "
            "that information in your response. If you cannot find the answer, state that you couldn't "
            "find the information. Keep your answers concise and direct."
        )),
        MessagesPlaceholder(variable_name="messages")
    ]
)
llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

if llm_provider == "openai":
    llm = ChatOpenAI(model="gpt-4o")
elif llm_provider == "google":
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
else:
    raise ValueError(f"Unsupported LLM_PROVIDER: {llm_provider}")
agent = prompt | llm.bind_tools(tools)

# 2. Define the Nodes
def agent_node(state: AgentState):
    """
    The "brain" of the agent. This node decides what to do next.
    """
    result = agent.invoke(state)
    return {"messages": [result]}

tool_node = ToolNode(tools)

# 3. Define the Logic (Conditional Edge)
def should_continue(state: AgentState):
    """
    This function decides whether to continue using tools or to end the graph flow.
    """
    if state["messages"][-1].tool_calls:
        return "action"
    return END

# 4. Build the Graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("action", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
)
graph.add_edge("action", "agent")

runnable = graph.compile()
