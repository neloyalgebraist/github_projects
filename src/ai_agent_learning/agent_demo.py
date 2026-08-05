"""Command-line entry point for the ReAct agent.

    python -m ai_agent_learning.agent_demo
    python -m ai_agent_learning.agent_demo "What is the weather in Tokyo?"

Run it with no argument and it uses the original demo question — the one that
forces the agent to chain two tools: search for the capital, then look up its
weather.
"""

from __future__ import annotations

import argparse

from ai_agent_learning.agent import build_agent
from ai_agent_learning.config import require_keys

DEFAULT_QUESTION = "Find the capital of India and then find its current weather."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ask the ReAct agent a question.")
    parser.add_argument(
        "question",
        nargs="?",
        default=DEFAULT_QUESTION,
        help="the question to ask (defaults to the two-tool demo question)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="hide the Thought/Action/Observation trace",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    require_keys()

    agent = build_agent(verbose=not args.quiet)
    result = agent.invoke({"input": args.question})

    print("\n" + "=" * 60)
    print("QUESTION:", args.question)
    print("ANSWER:  ", result["output"])
    print(f"({len(result.get('intermediate_steps', []))} tool call(s) used)")


if __name__ == "__main__":
    main()
