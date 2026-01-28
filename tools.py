from langchain_core.tools import tool
from duckduckgo_search import DDGS
import wikipedia

# Search tool using DuckDuckGo
@tool
def search_tool(query: str) -> str:
    """Search the internet for information."""
    try:
        results = DDGS().text(query, max_results=3)
        return str(results)
    except Exception as e:
        return f"Error searching: {str(e)}"

# Wikipedia tool
@tool
def wiki_tool(query: str) -> str:
    """Search Wikipedia for information."""
    try:
        result = wikipedia.summary(query)
        return result
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

# Save tool to save research to a file
@tool
def save_tool(content: str, filename: str = "research_output.txt") -> str:
    """Save research content to a file."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Content saved to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"
