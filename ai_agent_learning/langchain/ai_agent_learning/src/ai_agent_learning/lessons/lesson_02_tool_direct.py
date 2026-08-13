"""Lesson 2 — calling tools directly, with no model involved.

Point of the lesson: a tool is just a function. Here *you* decide when to call
it and what to pass. In Lesson 3 the model makes those decisions instead — and
that difference is the whole of what makes something an agent.

Note how much text one search returns. All of it would land in the model's
context, on every subsequent step of a loop. That is why max_results exists.

    python -m ai_agent_learning.lessons.lesson_02_tool_direct
"""

from __future__ import annotations

from ai_agent_learning.config import require_keys
from ai_agent_learning.tools import build_search_tool, get_weather_data

PREVIEW_CHARS = 300


def main() -> None:
    require_keys()

    search_tool = build_search_tool(max_results=2)
    results = search_tool.invoke("Give me the latest news on AI")

    print("=" * 60)
    print(f"SEARCH returned {len(results)} results\n")
    for item in results:
        print(f"- {item['title']}")
        print(f"  {item['url']}")
        print(f"  {item['content'][:PREVIEW_CHARS].strip()}...\n")

    total_chars = sum(len(item["content"]) for item in results)
    print(f"(~{total_chars} characters of content — this is what fills a context window)")

    print("=" * 60)
    print("WEATHER tool, called directly:\n")
    # .invoke() rather than calling get_weather_data("Paris") — the @tool
    # decorator wraps the function in a BaseTool object.
    print(get_weather_data.invoke({"city": "Paris"}))


if __name__ == "__main__":
    main()
