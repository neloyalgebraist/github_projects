"""Lesson 1 — a model on its own, with no tools.

Point of the lesson: the model has no clock, no filesystem, no internet. Ask
it the date and it cannot answer. That gap is the entire reason agents exist —
not that the model needs to be smarter, but that it needs access.

    python -m ai_agent_learning.lessons.lesson_01_llm_call
"""

from __future__ import annotations

from ai_agent_learning.agent import build_llm
from ai_agent_learning.config import require_keys

QUESTIONS = [
    "What year is it?",  # needs a clock it does not have
    "Explain what an API is in two sentences.",  # answerable from memory
]


def main() -> None:
    require_keys()
    llm = build_llm()

    for question in QUESTIONS:
        response = llm.invoke(question)

        print("=" * 60)
        print("Q:", question)
        # .content holds the text. The response itself is an AIMessage object
        # carrying metadata too — model responses are structures, not strings.
        print("A:", response.content)

        usage = response.usage_metadata or {}
        print(
            f"   tokens in={usage.get('input_tokens')} "
            f"out={usage.get('output_tokens')}"
        )


if __name__ == "__main__":
    main()
