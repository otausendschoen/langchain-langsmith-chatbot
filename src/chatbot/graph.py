import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .state import AgentState
from .tools import tools

# 1. Define the Agent
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's request only based on the given context."),
        MessagesPlaceholder(variable_name="messages")
    ]
)
llm = ChatOpenAI(model="gpt-4o")
agent = prompt | llm.bind_tools(tools)

# 2. Define the Nodes
def agent_node(state: AgentState):
    """
    The "brain" of the agent. This node decides what to do next.
    """
    result = agent.invoke(state)
    return {"messages": result}

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
