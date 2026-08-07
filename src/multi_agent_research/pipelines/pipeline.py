import re
from dataclasses import dataclass, field
from typing import Iterator, Literal

from langchain_core.messages import ToolMessage

from multi_agent_research.agents.agents import (
    DEFAULT_MODEL,
    build_critic_chain,
    build_reader_agent,
    build_search_agent,
    build_writer_chain,
)

# (key, short label, what the stage is doing while it runs)
STAGES: list[tuple[str, str, str]] = [
    ("search", "Search", "Scanning the web for primary sources"),
    ("read", "Read", "Scraping the most relevant source in full"),
    ("write", "Write", "Drafting the research report"),
    ("critique", "Critique", "Reviewing the draft for rigour"),
]

STAGE_LABELS = {key: label for key, label, _ in STAGES}

_URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")


@dataclass
class Event:
    """One transition in the pipeline, emitted so a UI can render progress live."""

    stage: str
    status: Literal["start", "done"]
    content: str = ""


@dataclass
class Research:
    """Everything the pipeline produced, in one place."""

    topic: str
    model: str = DEFAULT_MODEL
    search_summary: str = ""
    search_findings: str = ""  # raw tool output, the only place URLs survive intact
    scraped_content: str = ""
    report: str = ""
    feedback: str = ""
    sources: list[str] = field(default_factory=list)


def _tool_output(messages) -> str:
    """Join every ToolMessage in an agent run.

    The agent's final AIMessage is a prose summary and routinely drops the URLs
    the tool returned. Reading the ToolMessages directly is what keeps the
    sources available to later stages.
    """
    return "\n\n".join(
        str(m.content) for m in messages if isinstance(m, ToolMessage) and m.content
    )


def _unique_urls(*texts: str) -> list[str]:
    seen: dict[str, None] = {}
    for text in texts:
        for url in _URL_RE.findall(text or ""):
            seen.setdefault(url.rstrip(".,;)"), None)
    return list(seen)


def stream_research(
    topic: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.0,
) -> Iterator[Event | Research]:
    """Run the four-stage pipeline, yielding an Event per transition.

    The final item yielded is the completed Research object.
    """
    research = Research(topic=topic, model=model)

    # Stage 1 - search
    yield Event("search", "start")
    search_agent = build_search_agent(model, temperature)
    search_result = search_agent.invoke(
        {
            "messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic}")
            ]
        }
    )
    research.search_summary = search_result["messages"][-1].content
    research.search_findings = _tool_output(search_result["messages"])
    yield Event("search", "done", research.search_summary)

    # Stage 2 - read
    yield Event("read", "start")
    reader_agent = build_reader_agent(model, temperature)
    # Feed the raw tool output first: it carries the URLs the reader needs to
    # have something to scrape at all.
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{research.search_findings[:4000]}",
                )
            ]
        }
    )
    research.scraped_content = reader_result["messages"][-1].content
    scraped_raw = _tool_output(reader_result["messages"])
    yield Event("read", "done", research.scraped_content)

    research.sources = _unique_urls(
        research.search_findings, research.search_summary, scraped_raw
    )

    # Stage 3 - write
    yield Event("write", "start")
    research_combined = (
        f"SEARCH RESULTS:\n{research.search_findings}\n\n"
        f"SEARCH SUMMARY:\n{research.search_summary}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{research.scraped_content}"
    )
    research.report = build_writer_chain(model, temperature).invoke(
        {"topic": topic, "research": research_combined}
    )
    yield Event("write", "done", research.report)

    # Stage 4 - critique
    yield Event("critique", "start")
    research.feedback = build_critic_chain(model, temperature).invoke(
        {"report": research.report}
    )
    yield Event("critique", "done", research.feedback)

    yield research


def research_pipeline(
    topic: str, model: str = DEFAULT_MODEL, temperature: float = 0.0
) -> Research:
    """Console entry point: run the pipeline and print each stage as it lands."""
    rule = "=" * 60
    result = Research(topic=topic)

    for item in stream_research(topic, model, temperature):
        if isinstance(item, Research):
            result = item
            continue
        if item.status == "start":
            step = [i for i, (k, _, _) in enumerate(STAGES, 1) if k == item.stage][0]
            doing = next(d for k, _, d in STAGES if k == item.stage)
            print(f"\n{rule}\nStep {step} - {STAGE_LABELS[item.stage]}: {doing} ...\n{rule}")
        else:
            print(f"\n{item.content}")

    if result.sources:
        print(f"\n{rule}\nSources\n{rule}")
        for url in result.sources:
            print(f"- {url}")

    return result
