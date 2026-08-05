import os
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# load_dotenv() fails silently if it can't find .env, so check the keys
# actually arrived instead of hitting a confusing auth error later.
for key in ("GROQ_API_KEY", "TAVILY_API_KEY"):
    if not os.getenv(key):
        raise SystemExit(f"{key} is not set — check that .env exists in the project root")

search_tool = TavilySearchResults(max_results=3)

result = search_tool.invoke("Give me the latest news on AI")
print(result)
