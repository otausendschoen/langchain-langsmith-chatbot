from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    Represents the state of our agent.
    """
    messages: Annotated[list[BaseMessage], operator.add]
