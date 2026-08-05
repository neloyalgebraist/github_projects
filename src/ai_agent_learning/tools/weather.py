"""Current-weather tool, backed by the Weatherstack API."""

from __future__ import annotations

import requests
from langchain.tools import tool

from ai_agent_learning.config import get_key

API_URL = "http://api.weatherstack.com/current"
TIMEOUT_SECONDS = 10


@tool
def get_weather_data(city: str) -> str:
    """Get the current weather for a city.

    Use this when the user asks about weather, temperature, or conditions in a
    named place. Pass a single city name, for example "New Delhi" or "Paris".
    """
    # This docstring is not a comment: @tool sends it to the model as the
    # tool's description. It is the only thing the model knows about this
    # function, so it is prompt engineering — keep it precise.
    try:
        response = requests.get(
            API_URL,
            params={"access_key": get_key("WEATHERSTACK_API_KEY"), "query": city},
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        # Return the failure as text instead of raising. A raised exception
        # kills the agent loop; a returned string lets the model read the
        # problem and decide what to do next.
        return f"Weather lookup for {city} failed: {exc}"

    if "current" not in data:
        detail = data.get("error", {}).get("info", "no 'current' field in response")
        return f"Could not fetch weather for {city}: {detail}"

    current = data["current"]
    descriptions = current.get("weather_descriptions") or ["unknown"]
    return (
        f"City: {city}\n"
        f"Temperature: {current['temperature']}C\n"
        f"Weather: {descriptions[0]}\n"
        f"Humidity: {current['humidity']}%"
    )
