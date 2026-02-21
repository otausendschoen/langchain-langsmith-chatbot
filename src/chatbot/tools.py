import os
from langchain_tavily import TavilySearch

tools = []
if os.getenv("TAVILY_API_KEY"):
    tool = TavilySearch(max_results=2) # Changed class name
    tools.append(tool)
else:
    print("Warning: TAVILY_API_KEY not found. Web search tool will not be available.")
