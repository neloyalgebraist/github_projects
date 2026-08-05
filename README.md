# Multi-Agent Research

A research assistant built from multiple cooperating agents: one plans, others
gather and read sources, another synthesises the result.

> **Status: scaffold.** The structure and dependencies are in place; the agent
> code is not written yet.

## Quick start

```bash
# 1. Install dependencies
uv sync

# 2. Add your API keys
cp .env.example .env
$EDITOR .env

# 3. Run
uv run streamlit run app.py          # web UI
uv run multi-agent-research          # command line
```

### API keys

`.env` is git-ignored; `.env.example` documents the names without the values.

| Variable | Used for | Get one at |
|---|---|---|
| `GROQ_API_KEY` | Chat model inference | [console.groq.com](https://console.groq.com/keys) |
| `TAVILY_API_KEY` | Web search | [app.tavily.com](https://app.tavily.com) |

## Project layout

```
.
├── app.py                          Streamlit UI
├── .env.example                    Required keys, without the values
├── pyproject.toml                  Dependencies (single source of truth)
└── src/multi_agent_research/
    ├── main.py                     CLI entry point
    ├── agents/                     One module per agent role
    ├── tools/                      Capabilities the agents can call
    └── pipelines/                  Orchestration — how agents hand off
```

Each package's `__init__.py` is its public surface: re-export from there so
callers write `from multi_agent_research.agents import Researcher` and the file
layout inside stays free to change.

## Notes on the stack

- **LangChain 1.x.** `AgentExecutor` and the text-parsed ReAct loop do not exist
  in this version; agents are built with `create_agent()` on top of LangGraph
  and use native tool calling instead of parsing `Action:` lines out of text.
- **`starlette<1.4` is pinned deliberately.** Streamlit 1.61 calls Starlette's
  `GZipResponder` without the `thread_minimum_size` argument that Starlette 1.4
  made required, so every gzipped request — meaning every browser request —
  returns a 500. Streamlit's own pin is too loose to prevent it. Remove the pin
  once that is fixed upstream.
- **Tool docstrings are prompts.** The `@tool` decorator sends a function's
  docstring to the model as the tool's description; it is the only thing the
  model knows about it.
- **Search results are untrusted input.** They are data fetched from the web,
  not instructions — the entry point for prompt injection.

## Roadmap

- [ ] Define the agent roles and their hand-offs
- [ ] Search and page-extraction tools (`trafilatura` / `readability-lxml`)
- [ ] Pipeline orchestration
- [ ] Streamlit UI with per-agent traces
- [ ] Evaluations

## Stack

Python 3.13 · [uv](https://docs.astral.sh/uv/) · LangChain 1.x · Groq ·
Tavily · Streamlit
