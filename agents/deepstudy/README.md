# 🔬 DeepStudy Professional

A modern, agentic multi-model research pipeline built with **LangGraph**, **Mistral AI**, and **Groq**. 

This research assistant uses a specialized multi-agent architecture to plan, search (Web + ArXiv), critique, and synthesize high-quality reports — **all using free API tiers.**

## 🧠 Architecture

1.  **Orchestrator (Mistral Small):** Plans the research and generates sub-queries.
2.  **Search Agent (Tavily + ArXiv):** Gathers sources from the web and academic databases.
3.  **Reader Agent (Llama 3.3 70B):** Extracts key findings from sources.
4.  **Critic Agent (Llama 3.3 70B):** Evaluates findings for quality and contradictions.
5.  **Synthesizer (Mistral Small):** Drafts a coherent, grounded answer.
6.  **Output Agent (Llama 3.1 8B):** Polishes the report and adds formatted citations.

## 🚀 Getting Started

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) (Fast Python package manager)
- API Keys for: [Mistral AI](https://console.mistral.ai/), [Groq](https://console.groq.com/), and [Tavily](https://tavily.com/)

### 2. Installation
```bash
git clone <your-repo-url>
cd deepstudy
uv sync
```

### 3. Configuration
Create a `.env` file in the root directory:
```bash
MISTRAL_API_KEY=your_mistral_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Running the App
```bash
uv run streamlit run app.py
```

## 🛠 Built With
- **LangGraph:** For stateful, multi-agent orchestration.
- **Streamlit:** For the professional research UI.
- **Mistral AI & Groq:** For high-performance, free-tier LLM processing.
- **Pydantic:** For robust type-safe state management.

---
*Created with the help of Gemini CLI*
