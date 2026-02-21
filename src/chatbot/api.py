from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv # Import load_dotenv
import os

load_dotenv() # Call load_dotenv() at the top

from .graph import runnable

# Create a FastAPI app instance
app = FastAPI(
    title="LangChain Chatbot Server",
    description="A simple API server for the LangChain chatbot.",
    version="1.0.0",
)

# Define a Pydantic model for the request body
class ChatRequest(BaseModel):
    message: str

# Define the /chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Receives a message from the user, gets the chatbot's response, and returns it.
    """
    response = runnable.invoke({"messages": [HumanMessage(content=request.message)]})
    agent_response = response["messages"][-1].content
    return {"response": agent_response}
