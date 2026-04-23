from langgraph.graph import StateGraph, START, END
from core.state import ResearchState
from agents.agents import (
    orchestrator_agent, search_agent, reader_agent,
    critic_agent, synthesis_agent, output_agent
)

def build_pipeline():
    workflow = StateGraph(ResearchState)

    workflow.add_node("orchestrator", orchestrator_agent)
    workflow.add_node("search", search_agent)
    workflow.add_node("reader", reader_agent)
    workflow.add_node("critic", critic_agent)
    workflow.add_node("synthesizer", synthesis_agent)
    workflow.add_node("output", output_agent)

    workflow.add_edge(START, "orchestrator")
    workflow.add_edge("orchestrator", "search")
    workflow.add_edge("search", "reader")
    workflow.add_edge("reader", "critic")
    workflow.add_edge("critic", "synthesizer")
    workflow.add_edge("synthesizer", "output")
    workflow.add_edge("output", END)

    return workflow.compile()

def run_research(query: str):
    pipeline = build_pipeline()
    return pipeline.invoke({"query": query})

if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "How does photosynthesis work?"
    print(run_research(q)["final_report"])
