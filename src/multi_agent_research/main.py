import sys

from multi_agent_research.pipelines.pipeline import research_pipeline

DEFAULT_TOPIC = "The impact of AI on the job market in 2026"


def main() -> None:
    topic = " ".join(sys.argv[1:]).strip() or DEFAULT_TOPIC
    research_pipeline(topic)


if __name__ == "__main__":
    main()
