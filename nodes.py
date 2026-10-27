"""The 4 LangGraph nodes. Each reads the state and returns only the keys it updates."""
from langchain_core.messages import HumanMessage, SystemMessage

from llm import get_llm
from schemas import JobInfo, JobClassification, TopSkills, HiringReport
from state import JobState


def _ask(schema, system_prompt: str, user_prompt: str):
    """Call the LLM and force the answer into a Pydantic schema."""
    structured_llm = get_llm().with_structured_output(schema)
    return structured_llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])


# ---------- Node 1: Information Extraction ----------
def extract_info(state: JobState) -> dict:
    try:
        result = _ask(
            JobInfo,
            "You extract facts from job descriptions. Only use what is written in the text. "
            "If something is missing write 'Not specified'. Skills must be short names, no sentences.",
            f"Job description:\n\n{state['job_description']}",
        )
        return {"job_info": result.model_dump()}
    except Exception as e:
        return {"error": f"Node 1 (extraction) failed: {e}"}


# ---------- Node 2: Job Classification ----------
def classify_job(state: JobState) -> dict:
    try:
        info = state["job_info"]
        result = _ask(
            JobClassification,
            "You classify jobs by seniority level and broad job category.",
            f"Title: {info['job_title']}\nExperience: {info['required_experience']}\n"
            f"Skills: {', '.join(info['required_skills'])}\n\n"
            f"Full description:\n{state['job_description']}",
        )
        return {"classification": result.model_dump()}
    except Exception as e:
        return {"error": f"Node 2 (classification) failed: {e}"}


# ---------- Node 3: Top 3 Skills ----------
def rank_top_skills(state: JobState) -> dict:
    try:
        info = state["job_info"]
        result = _ask(
            TopSkills,
            "You pick the 3 most important skills for a role. Prefer skills from the given list. "
            "Return exactly 3, ranked 1 (most important) to 3.",
            f"Role: {info['job_title']} ({state['classification']['job_category']})\n"
            f"Skills: {', '.join(info['required_skills'])}\n\n"
            f"Job description:\n{state['job_description']}",
        )
        return {"top_skills": [s.model_dump() for s in result.top_skills[:3]]}
    except Exception as e:
        return {"error": f"Node 3 (top skills) failed: {e}"}


# ---------- Node 4: Report Generation ----------
def generate_report(state: JobState) -> dict:
    try:
        info, cls, top = state["job_info"], state["classification"], state["top_skills"]

        summary_llm = get_llm().invoke([
            SystemMessage(content="Write a 2-sentence hiring summary for a recruiter. Plain text only."),
            HumanMessage(content=f"Job info: {info}\nClassification: {cls}\nTop skills: {top}"),
        ])
        summary = summary_llm.content if isinstance(summary_llm.content, str) else str(summary_llm.content)

        report = HiringReport(
            job_title=info["job_title"],
            company_name=info["company_name"],
            required_experience=info["required_experience"],
            required_skills=info["required_skills"],
            seniority_level=cls["seniority_level"],
            job_category=cls["job_category"],
            top_skills=top,
            summary=summary.strip(),
        )
        return {"report": report.model_dump()}
    except Exception as e:
        return {"error": f"Node 4 (report) failed: {e}"}
