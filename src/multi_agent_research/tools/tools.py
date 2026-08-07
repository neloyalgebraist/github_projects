from langchain.tools import tool
import requests
import trafilatura
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs, contents."""
    results = tavily.search(query=query, max_results=5)

    out = []

    for r in results["results"]:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}\n")

    return "\n-----\n".join(out)


def scrape_url(url: str, max_chars: int = 4000) -> str:
    """Read a web page and return its main article text.

    Use this after web_search when a search result looks worth reading in full.
    Strips navigation, ads, cookie banners and other boilerplate, and returns
    the title, the URL and the article body.
    """
    # Many sites reject the default python-requests user agent outright.
    headers = {"User-Agent": "Mozilla/5.0 (compatible; multi-agent-research/0.1)"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Return the failure as text rather than raising: an agent can read a
        # string and try something else, but an exception ends its turn.
        return f"Could not fetch {url}: {exc}"

    if "html" not in response.headers.get("Content-Type", "").lower():
        return f"Skipped {url}: not an HTML page (PDFs and images aren't supported)"

    text = trafilatura.extract(
        response.text,
        url=url,
        include_comments=False,
        include_tables=True,
        favor_precision=True,  # prefer dropping junk over keeping everything
    )

    if not text:
        return f"No readable article content found at {url}"

    metadata = trafilatura.extract_metadata(response.text)
    title = metadata.title if metadata and metadata.title else "(no title)"

    # A long page can be tens of thousands of characters. Every one of them
    # would sit in the model's context on every later step of the loop.
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + f"\n\n[truncated at {max_chars} characters]"

    return f"Title: {title}\nURL: {url}\n\n{text}"
