"""Builds the LangGraph workflow and exposes run_analysis()."""
from langgraph.graph import StateGraph, START, END

from nodes import extract_info, classify_job, rank_top_skills, generate_report
from state import JobState
from validation import validate_job_description


def _continue_or_end(next_node: str):
    """Stop the graph early if a node stored an error in the state."""
    def router(state: JobState) -> str:
        return END if state.get("error") else next_node
    return router


def build_graph():
    g = StateGraph(JobState)
    g.add_node("extract_info", extract_info)
    g.add_node("classify_job", classify_job)
    g.add_node("rank_top_skills", rank_top_skills)
    g.add_node("generate_report", generate_report)

    g.add_edge(START, "extract_info")
    g.add_conditional_edges("extract_info", _continue_or_end("classify_job"))
    g.add_conditional_edges("classify_job", _continue_or_end("rank_top_skills"))
    g.add_conditional_edges("rank_top_skills", _continue_or_end("generate_report"))
    g.add_edge("generate_report", END)
    return g.compile()


def run_analysis(job_description: str) -> dict:
    """Validate input, run the graph, return {'report': ...} or {'error': ...}."""
    ok, message = validate_job_description(job_description)
    if not ok:
        return {"error": message}

    final_state = build_graph().invoke({"job_description": job_description.strip()})
    if final_state.get("error"):
        return {"error": final_state["error"]}
    return {"report": final_state["report"]}
