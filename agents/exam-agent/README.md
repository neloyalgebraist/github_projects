# 🎓 Indian Government Exam Research Agent

An autonomous research pipeline built with **LangGraph**, **Groq (Llama 3)**, and **Tavily Search**. This agent automates the process of finding upcoming government exams in India, extracting key dates/fees, and generating detailed study plans.

## 🧠 Agent Architecture

The agent follows a linear stateful graph:
1.  **Search Node:** Uses Tavily to find the latest web listings for exams.
2.  **Extraction Node:** Uses Llama 3 (via Groq) to parse unstructured web data into structured Pydantic models.
3.  **Selection Node:** Filters and ranks the top 5 most relevant exams.
4.  **Deep Research Node:** Performs targeted searches for syllabus, preparation timelines, and study resources.
5.  **Reporting Node:** Synthesizes all data into a formatted Markdown report.

## 🚀 Getting Started

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Groq API Key](https://console.groq.com/)
- [Tavily API Key](https://tavily.com/)

### 2. Installation
```bash
# Clone the repository (if applicable)
cd exam-agent
uv sync
```

### 3. Configuration
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Usage

#### CLI Mode
```bash
uv run main.py "upcoming SSC and UPSC exams 2026"
```

#### Streamlit UI
```bash
uv run streamlit run streamlit_app.py
```

## 🛠 Built With
- **LangGraph:** Stateful multi-agent orchestration.
- **Groq:** High-speed LLM inference (Llama 3.3 70B).
- **Tavily:** Search engine optimized for LLMs.
- **Pydantic:** Type-safe state management.
- **Streamlit:** Professional web interface.
