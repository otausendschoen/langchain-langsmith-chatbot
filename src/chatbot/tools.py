import os
from langchain_community.tools.tavily_search import TavilySearchResults

tools = []
if os.getenv("TAVILY_API_KEY"):
    tool = TavilySearchResults(max_results=2)
    tools.append(tool)
else:
    print("Warning: TAVILY_API_KEY not found. Web search tool will not be available.")
