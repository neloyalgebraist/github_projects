"""Tools the agent can call.

Anything importable from here is a capability the agent can be given.
`build_tools()` is the single list the agent and the Streamlit app share, so
adding a tool in one place makes it available everywhere.
"""

from __future__ import annotations

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import BaseTool

from ai_agent_learning.tools.weather import get_weather_data

DEFAULT_SEARCH_RESULTS = 3


def build_search_tool(max_results: int = DEFAULT_SEARCH_RESULTS) -> BaseTool:
    """Web search via Tavily.

    `max_results` is a cost and context control, not just a preference: every
    result is fed into the model's context on each subsequent loop step.
    """
    return TavilySearchResults(max_results=max_results)


def build_tools(max_search_results: int = DEFAULT_SEARCH_RESULTS) -> list[BaseTool]:
    """The full tool set the agent gets."""
    return [build_search_tool(max_search_results), get_weather_data]


__all__ = ["build_search_tool", "build_tools", "get_weather_data"]
