from pydantic import BaseModel, Field
from typing import List, Annotated, Optional
import operator

class ResearchState(BaseModel):
    # --- Input ---
    query: str                          # Original user question

    # --- Orchestrator output ---
    sub_queries: List[str] = Field(default_factory=list)
    plan: str = ""

    # --- Search Agent output ---
    search_results: List[dict] = Field(default_factory=list)
    arxiv_papers: List[dict] = Field(default_factory=list)

    # --- Reader Agent output ---
    extracted_findings: List[dict] = Field(default_factory=list)

    # --- Critic Agent output ---
    critique: str = ""
    quality_score: float = 0.0

    # --- Synthesis Agent output ---
    synthesis: str = ""

    # --- Output Agent output ---
    final_report: str = ""
    citations: List[str] = Field(default_factory=list)

    # --- Metadata ---
    current_step: str = "start"
    errors: Annotated[List[str], operator.add] = Field(default_factory=list)
