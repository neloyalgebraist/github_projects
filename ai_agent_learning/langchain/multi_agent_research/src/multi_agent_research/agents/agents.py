from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from multi_agent_research.tools.tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile"

# Every model here supports tool calling, which the search and reader agents need.
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.6-27b",
    "llama-3.1-8b-instant",
]


def get_llm(model: str = DEFAULT_MODEL, temperature: float = 0.0) -> ChatGroq:
    """Build the chat model.

    Deliberately not a module-level singleton: constructing ChatGroq needs
    GROQ_API_KEY, and doing that at import time makes a missing key blow up as
    an ImportError halfway up a stack trace instead of a message the UI can show.
    """
    return ChatGroq(model=model, temperature=temperature)


# Search Agent
def build_search_agent(model: str = DEFAULT_MODEL, temperature: float = 0.0):
    return create_agent(
        model=get_llm(model, temperature),
        tools=[web_search],
        system_prompt=(
            "You are a research scout. Always use the web_search tool before answering. "
            "When you summarise what you found, reproduce every source URL verbatim next "
            "to the claim it supports. Never invent a URL."
        ),
    )


# Reader Agent
def build_reader_agent(model: str = DEFAULT_MODEL, temperature: float = 0.0):
    return create_agent(
        model=get_llm(model, temperature),
        tools=[scrape_url],
        system_prompt=(
            "You are a close reader. You are given search results containing URLs. "
            "Pick the single most relevant URL and call the scrape_url tool on it. "
            "Then report the substantive content you read, keeping figures, dates and "
            "quotes intact. Always cite the URL you scraped."
        ),
    )


# Writer Agent
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert research writer. Write clear, structured and insightful reports.",
        ),
        (
            "human",
            """Write a detailed research report on the topic below.
    Topic: {topic}

    Research Gathered:
    {research}

    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well explained points)
    - Conclusion
    - Sources (list all URLs found in the research)

    Be detailed, factual and professional.
    """,
        ),
    ]
)


def build_writer_chain(model: str = DEFAULT_MODEL, temperature: float = 0.0):
    return writer_prompt | get_llm(model, temperature) | StrOutputParser()


# Critic Chain

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a sharp and constructive research critic. Be honest and specific.",
        ),
        (
            "human",
            """Review the research report below and evaluate it strictly.
    Report:
    {report}

    Respond in this exact format:

    Score: x/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...

    One line verdict:
    ...
    """,
        ),
    ]
)


def build_critic_chain(model: str = DEFAULT_MODEL, temperature: float = 0.0):
    return critic_prompt | get_llm(model, temperature) | StrOutputParser()
