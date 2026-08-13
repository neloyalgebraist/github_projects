"""The ReAct agent — built once here, reused by the CLI and the Streamlit app.

The whole agent is three objects:

    llm      the model that decides what to do
    tools    the things it is allowed to do
    prompt   the instructions telling it how to say what it wants to do

`AgentExecutor` is the loop that runs around them:
Thought -> Action -> Observation -> repeat, until the model says Final Answer.
"""

from __future__ import annotations

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain_groq import ChatGroq
from langsmith import Client

from ai_agent_learning.config import DEFAULT_MODEL, DEFAULT_TEMPERATURE
from ai_agent_learning.tools import build_tools

REACT_PROMPT = "hwchase17/react"

# Circuit breaker. Without a ceiling, a confused agent can loop until it
# exhausts your API credits. Five is plenty for a two-tool agent.
DEFAULT_MAX_ITERATIONS = 5


def build_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
) -> ChatGroq:
    """Create the chat model.

    No api_key argument: ChatGroq reads GROQ_API_KEY from the environment
    itself. Temperature stays at 0 for agents — higher values mean more varied
    phrasing, which is exactly what breaks a format-sensitive ReAct parser.
    """
    return ChatGroq(model=model, temperature=temperature)


def load_react_prompt():
    """Fetch the ReAct prompt template from LangChain Hub.

    `dangerously_pull_public_prompt` is required because a hub prompt is a
    serialized object downloaded from the internet and authored by a stranger.
    Treat it as untrusted input; the scary parameter name is deliberate.
    """
    return Client().pull_prompt(REACT_PROMPT, dangerously_pull_public_prompt=True)


def build_agent(
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    max_search_results: int = 3,
    tools: list[BaseTool] | None = None,
    llm: BaseLanguageModel | None = None,
    verbose: bool = False,
) -> AgentExecutor:
    """Assemble a ready-to-run ReAct agent."""
    llm = llm or build_llm(model=model, temperature=temperature)
    tools = tools if tools is not None else build_tools(max_search_results)

    agent = create_react_agent(llm=llm, tools=tools, prompt=load_react_prompt())

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        # Feed format mistakes back to the model as a correction instead of
        # raising. ReAct parses the model's raw text, so this fires often.
        handle_parsing_errors=True,
        max_iterations=max_iterations,
        return_intermediate_steps=True,
    )


def run_agent(question: str, **kwargs) -> dict:
    """Convenience wrapper: build an agent and answer one question."""
    return build_agent(**kwargs).invoke({"input": question})
