import json
from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage
from core.state import ResearchState
from core.models import get_orchestrator, get_reader, get_critic, get_synthesizer, get_output_formatter
from tools.search import tavily_search, arxiv_search

# --- Structured Output Models ---
class PlanSchema(BaseModel):
    plan: str = Field(description="A 3-5 step research plan")
    sub_queries: List[str] = Field(description="List of 3 search queries")

class ExtractionSchema(BaseModel):
    findings: List[str] = Field(description="List of key points extracted from source")
    relevance: str = Field(description="High/Medium/Low")

class CritiqueSchema(BaseModel):
    score: float = Field(description="Quality score 0.0-1.0")
    critique: str = Field(description="Constructive critique of the findings")

# --- Agents ---
def orchestrator_agent(state: ResearchState) -> ResearchState:
    llm = get_orchestrator().with_structured_output(PlanSchema)
    res = llm.invoke([
        SystemMessage(content="You are a research planner."),
        HumanMessage(content=f"Question: {state.query}")
    ])
    return state.model_copy(update={
        "plan": res.plan,
        "sub_queries": res.sub_queries,
        "current_step": "search"
    })

def search_agent(state: ResearchState) -> ResearchState:
    web, papers = [], []
    for q in state.sub_queries:
        web.extend(tavily_search(q, 2))
        papers.extend(arxiv_search(q, 2))
    return state.model_copy(update={
        "search_results": web[:6],
        "arxiv_papers": papers[:4],
        "current_step": "read"
    })

def reader_agent(state: ResearchState) -> ResearchState:
    llm = get_reader().with_structured_output(ExtractionSchema)
    findings = []
    sources = (state.search_results[:3] + state.arxiv_papers[:2])
    for s in sources:
        try:
            content = s.get("snippet") or s.get("abstract")
            res = llm.invoke(f"Extract findings for '{state.query}' from:\n{content}")
            findings.append({"title": s["title"], "url": s["url"], "points": res.findings})
        except: continue
    return state.model_copy(update={"extracted_findings": findings, "current_step": "critique"})

def critic_agent(state: ResearchState) -> ResearchState:
    llm = get_critic().with_structured_output(CritiqueSchema)
    context = json.dumps(state.extracted_findings, indent=2)
    res = llm.invoke(f"Evaluate these findings for the query '{state.query}':\n{context}")
    return state.model_copy(update={
        "quality_score": res.score,
        "critique": res.critique,
        "current_step": "synthesize"
    })

def synthesis_agent(state: ResearchState) -> ResearchState:
    llm = get_synthesizer()
    context = json.dumps(state.extracted_findings, indent=2)
    res = llm.invoke(f"Synthesize these findings into an answer for '{state.query}':\n{context}")
    return state.model_copy(update={"synthesis": res.content, "current_step": "output"})

def output_agent(state: ResearchState) -> ResearchState:
    llm = get_output_formatter()
    citations = [f"[{i+1}] {f['title']} ({f['url']})" for i, f in enumerate(state.extracted_findings)]
    res = llm.invoke(f"Polish this report and ensure professional formatting:\n{state.synthesis}")
    return state.model_copy(update={
        "final_report": res.content + "\n\n### Sources\n" + "\n".join(citations),
        "citations": citations,
        "current_step": "done"
    })
