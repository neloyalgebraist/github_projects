import os
import arxiv
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key: return []
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)
        return [{"title": r["title"], "url": r["url"], "snippet": r["content"], "source": "web"} for r in response.get("results", [])]
    except Exception as e:
        print(f"Tavily error: {e}")
        return []

def arxiv_search(query: str, max_results: int = 5) -> list[dict]:
    try:
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
        return [{
            "title": res.title,
            "authors": [a.name for a in res.authors[:3]],
            "abstract": res.summary[:800],
            "url": res.entry_id,
            "published": str(res.published.date()),
            "source": "arxiv"
        } for res in client.results(search)]
    except Exception as e:
        print(f"ArXiv error: {e}")
        return []
