from typing import List
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage
from core.state import ExamInfo, ExamState, ExamDetail
from core.models import get_model
from tools.search import tavily_search

class ExtractedExamSchema(BaseModel):
    exams: List[ExamInfo]

def search_exams_node(state: ExamState) -> ExamState:
    """Step 1: Find upcoming government exams using Tavily."""
    print("--- SEARCHING FOR EXAMS ---")
    results = tavily_search(state.query, max_results=6)
    return state.model_copy(update={"search_results": results})

def extract_exams_node(state: ExamState) -> ExamState:
    """Step 2: Extract structured data (Dates, Fees) from search snippets."""
    print("--- EXTRACTING EXAM DATA ---")
    llm = get_model().with_structured_output(ExtractedExamSchema)

    # Tavily returns 'content' or 'snippet'. The wrapper in tools/search.py returns the raw results.
    # Looking at the wrapper, it returns results as-is from client.search().
    # Standard Tavily response for results has 'content'.
    context = "\n".join([f"Source: {r['title']}\nContent: {r.get('content', r.get('snippet', ''))}" for r in state.search_results])
    
    res = llm.invoke([
        SystemMessage(content="You are an expert at extracting Indian government exam data. Extract Name, Start/End dates, Exam date, and Fees. Use 'N/A' for missing info."),
        HumanMessage(content=f"Extract exams from this data:\n\n{context}")
    ])
    return state.model_copy(update={"extracted_exams": res.exams})

def select_top_exams_node(state: ExamState) -> ExamState:
    """Step 3: Pick the top 5 exams for deeper research."""
    print("--- SELECTING TOP 5 ---")
    return state.model_copy(update={"top_exams": state.extracted_exams[:5]})

def research_syllabus_node(state: ExamState) -> ExamState:
    """Step 4: Research syllabus and resources for the top 5 exams."""
    print("--- RESEARCHING SYLLABUS & RESOURCES ---")
    llm = get_model().with_structured_output(ExamDetail)
    details = []

    for exam in state.top_exams:
        search_query = f"{exam.name} syllabus 2026-2027 preparation resources and timeline"
        results = tavily_search(search_query, max_results=3)
        context = "\n".join([r.get('content', r.get('snippet', '')) for r in results])

        res = llm.invoke([
            SystemMessage(content=f"Extract syllabus, prep time, and resources for {exam.name}."),
            HumanMessage(content=f"Context:\n{context}")
        ])
        details.append(res)

    return state.model_copy(update={"detailed_info": details})

def report_node(state: ExamState) -> ExamState:
    """Step 5: Format everything into a beautiful Markdown report."""
    print("--- GENERATING FINAL REPORT ---")

    table = "| Exam Name | App Start | App End | Exam Date | Fees |\n"
    table += "|-----------|------------|---------|-----------|-------|\n"

    for e in state.extracted_exams:
        table += f"| {e.name} | {e.app_start} | {e.app_end} | {e.exam_date} | {e.fees} |\n"

    details_md = "\n## Deep Dive: Top 5 Exams Syllabus & Resources\n"
    for d in state.detailed_info:
        details_md += f"\n### {d.name}\n"
        details_md += f"- **Preparation Time:** {d.time_to_complete}\n"
        details_md += f"- **Syllabus:** {d.syllabus}\n"
        details_md += "- **Resources:**\n"
        for r in d.resources:
            details_md += f"  - {r}\n"

    final_md = f"# Indian Government Exams Report\n\n{table}\n{details_md}"
    return state.model_copy(update={"final_report": final_md})






