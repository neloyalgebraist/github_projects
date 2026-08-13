import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


def tavily_search(query: str, max_results: int = 5):
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return []

    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query, search_depth="advanced", max_results=max_results
    )
    return response.get("results", [])
