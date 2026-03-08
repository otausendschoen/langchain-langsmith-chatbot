import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .graph import runnable

# 1. Create the FastAPI app instance FIRST
app = FastAPI(
    title="LangChain Chatbot Server",
    description="A simple API server for the LangChain chatbot.",
    version="1.0.0",
)

# 2. Mount static files
# This makes the "static" folder accessible via the "/static" URL path
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Define a Pydantic model for the request body
class ChatRequest(BaseModel):
    message: str

# 4. Define endpoints

# Serve the index.html file at the root URL
@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

# Stateless HTTP endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Receives a message from the user, gets the chatbot's response, and returns it.
    (Stateless)
    """
    response = runnable.invoke({"messages": [HumanMessage(content=request.message)]})
    agent_response = response["messages"][-1].content
    return {"response": agent_response}

# Stateful WebSocket endpoint
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Initialize message history for this WebSocket session
    message_history = []
    
    try:
        while True:
            # Receive message from the client
            data = await websocket.receive_text()
            
            # Append user message to history
            message_history.append(HumanMessage(content=data))
            
            # Invoke the agent with the full history
            response = runnable.invoke({"messages": message_history})
            
            # Get the agent's response and append to history
            agent_msg = response["messages"][-1]
            message_history.append(agent_msg)
            
            # Send the bot's response text back to the client
            await websocket.send_text(agent_msg.content)
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        # Note: Depending on the error, the socket might already be closed
        try:
            await websocket.close()
        except:
            pass
