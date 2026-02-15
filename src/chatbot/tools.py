from langchain_community.tools.tavily_search import TavilySearchResults

# Initialize the tool
tool = TavilySearchResults(max_results=2)

# Create a list of tools
tools = [tool]
