"""Central configuration: one place that knows about the environment.

Every other module imports from here instead of calling load_dotenv() itself.
That way the .env file is located exactly once, in a way that does not depend
on which directory you happen to run a script from.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# config.py lives at <root>/src/ai_agent_learning/config.py, so the project
# root is three levels up. Resolving it explicitly means `.env` is found
# whether you run a script, a REPL, or `streamlit run`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

# Every API key this project can use, and what it is for.
REQUIRED_KEYS: dict[str, str] = {
    "GROQ_API_KEY": "Groq — chat model inference (console.groq.com)",
    "TAVILY_API_KEY": "Tavily — web search tool (tavily.com)",
    "WEATHERSTACK_API_KEY": "Weatherstack — current weather tool (weatherstack.com)",
}

DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TEMPERATURE = 0.0


def missing_keys() -> list[str]:
    """Return the names of any required keys that are not set."""
    return [name for name in REQUIRED_KEYS if not os.getenv(name)]


def require_keys() -> None:
    """Exit immediately with a readable message if any key is missing.

    load_dotenv() returns False and carries on when it finds no .env, so
    without this check a missing key surfaces much later as a confusing
    authentication error from deep inside a library.
    """
    missing = missing_keys()
    if missing:
        lines = [f"  - {name}: {REQUIRED_KEYS[name]}" for name in missing]
        raise SystemExit(
            "Missing required environment variable(s):\n"
            + "\n".join(lines)
            + f"\n\nAdd them to {PROJECT_ROOT / '.env'} (see .env.example)."
        )


def get_key(name: str) -> str:
    """Fetch a key at the point of use, failing loudly if it is absent."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set — see .env.example")
    return value
