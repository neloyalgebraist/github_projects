# AI Agent Learning

Building an AI agent from first principles with LangChain, Groq, and Streamlit.

A **ReAct agent** that reasons about a question, decides which tools to call,
feeds the results back to itself, and loops until it has an answer. It can
search the web and look up live weather, and it chains them on its own — ask it
for the weather in India's capital and it will search for the capital first,
then use that answer as the input to the weather tool.

<!-- Add a screenshot of the Streamlit app here -->

## Quick start

```bash
# 1. Install dependencies (uv reads pyproject.toml)
uv sync

# 2. Add your API keys
cp .env.example .env
$EDITOR .env

# 3. Run the web app
uv run streamlit run app.py

# ...or the command line
uv run python -m ai_agent_learning.agent_demo
uv run python -m ai_agent_learning.agent_demo "What is the weather in Tokyo?"
```

### API keys

All three are free to obtain. `.env` is git-ignored; `.env.example` documents
the names without the values.

| Variable | Used for | Get one at |
|---|---|---|
| `GROQ_API_KEY` | Chat model inference | [console.groq.com](https://console.groq.com/keys) |
| `TAVILY_API_KEY` | Web search tool | [app.tavily.com](https://app.tavily.com) |
| `WEATHERSTACK_API_KEY` | Current weather tool | [weatherstack.com](https://weatherstack.com/dashboard) |

## Project layout

```
.
├── app.py                          Streamlit UI — renders the agent's reasoning live
├── .env.example                    Required keys, without the values
├── pyproject.toml                  Dependencies (single source of truth)
└── src/ai_agent_learning/
    ├── config.py                   Loads .env once; validates keys
    ├── agent.py                    build_agent() — the reusable ReAct core
    ├── agent_demo.py               CLI entry point
    ├── tools/
    │   ├── __init__.py             build_tools() — the shared tool set
    │   └── weather.py              Weatherstack tool
    └── lessons/
        ├── lesson_01_llm_call.py     A model alone, with no tools
        └── lesson_02_tool_direct.py  Tools alone, with no model
```

`agent.py` is the only place the agent is assembled, so the CLI and the web app
are guaranteed to behave identically.

## The lessons

Each runs standalone and demonstrates one idea. They are kept as executable
scripts rather than commented-out code, because commented code never runs and
so breaks silently when a library changes.

```bash
uv run python -m ai_agent_learning.lessons.lesson_01_llm_call
uv run python -m ai_agent_learning.lessons.lesson_02_tool_direct
```

**Lesson 1 — a model with no tools.** Ask it the year and it cannot answer: it
has no clock, no filesystem, no internet. That gap is the reason agents exist.
The model does not need to be smarter, it needs *access*.

**Lesson 2 — tools with no model.** A tool is just a function. Here you decide
when to call it and with what. Note how many characters one search returns:
all of it lands in the model's context on every later step of a loop.

**Lesson 3 — the agent** (`agent_demo.py` / `app.py`). The model makes those
decisions instead of you. That difference is the whole of what makes something
an agent.

## How the agent works

```
Thought:      I should search for this          ← the model decides
Action:       tavily_search_results_json        ← the model picks a tool
Action Input: "capital of India"                ← the model writes the argument
Observation:  [results...]                      ← the result is fed back in
Thought:      I now know the final answer       ← the model decides it is done
Final Answer: New Delhi
```

That is the entire mechanism. `AgentExecutor` is a `while` loop around a model
that can request tool calls; the ReAct prompt is what teaches it to write
`Action:` lines a parser can read.

### Notes on the implementation

- **`handle_parsing_errors=True`** — ReAct parses the model's raw text, so a
  small deviation from the format would otherwise raise. This feeds the error
  back as a correction instead.
- **`max_iterations`** — a circuit breaker. Without a ceiling, a confused agent
  can loop until it exhausts your API credits.
- **`temperature=0`** — higher values vary phrasing, which is exactly what
  breaks a format-sensitive parser.
- **Tool docstrings are prompts.** The `@tool` decorator sends a function's
  docstring to the model as the tool's description; it is the only thing the
  model knows about it. When a tool misfires, rewrite the docstring before
  touching the logic.
- **`dangerously_pull_public_prompt`** — a LangChain Hub prompt is a serialized
  object downloaded from the internet. Treat it as untrusted input.
- **Search results are untrusted too.** They are data the program fetched from
  the web, not instructions. Feeding them to a model is the entry point for
  prompt injection.

## Roadmap

- [x] Raw model calls, tokens, and cost
- [x] Tools, and calling them directly
- [x] A ReAct agent that chains tools
- [x] Streamlit UI with live reasoning
- [ ] Hand-written agent loop, without `AgentExecutor`
- [ ] Conversation memory across turns
- [ ] Context engineering — trimming what reaches the model
- [ ] Evaluations
- [ ] Native tool calling instead of text-parsed ReAct

## Stack

Python 3.13 · [uv](https://docs.astral.sh/uv/) · LangChain 0.3 ·
Groq (`llama-3.3-70b-versatile`) · Tavily · Weatherstack · Streamlit
