from langgraph.graph import StateGraph, START, END
from core.state import ExamState
from agents.agents import (
    search_exams_node,
    extract_exams_node,
    select_top_exams_node,
    research_syllabus_node,
    report_node,
)


def build_exam_pipeline():
    workflow = StateGraph(ExamState)

    workflow.add_node("search", search_exams_node)
    workflow.add_node("extract", extract_exams_node)
    workflow.add_node("select_top", select_top_exams_node)
    workflow.add_node("research_syllabus", research_syllabus_node)
    workflow.add_node("generate_report", report_node)

    workflow.add_edge(START, "search")
    workflow.add_edge("search", "extract")
    workflow.add_edge("extract", "select_top")
    workflow.add_edge("select_top", "research_syllabus")
    workflow.add_edge("research_syllabus", "generate_report")
    workflow.add_edge("generate_report", END)

    return workflow.compile()


def run_exam_research(query: str):
    """Utility function to run the graph for a given query."""
    app = build_exam_pipeline()
    initial_state = {"query": query}
    return app.invoke(initial_state)
