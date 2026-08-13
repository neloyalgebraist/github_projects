# My all github projects

AI agent work, grouped by the framework each project is built on.

## Layout

```
ai_agent_learning/
├── langchain/
│   ├── ai_agent_learning/      lessons, tools, ReAct agent + Streamlit app
│   └── multi_agent_research/   multi-agent research pipeline
└── langgraph/
    ├── deepstudy/              study agent (LangGraph + Streamlit)
    ├── exam-agent/             exam-question agent
    ├── langgraph-test/         LangGraph workflow scratchpad
    └── langgraph_projects/     LangGraph course exercises
```

`langchain/` holds the projects built directly on LangChain; `langgraph/`
holds the ones that use LangGraph for graph/state orchestration.

## Running a project

Each project is a self-contained `uv` project:

```sh
cd ai_agent_learning/<framework>/<project>
uv sync
```

Every project reads its API keys from a local `.env` (see the project's
`.env.example` where present). `.env` files are gitignored and must never be
committed. Keys used across these projects: `GROQ_API_KEY`, `TAVILY_API_KEY`,
`WEATHERSTACK_API_KEY`.
