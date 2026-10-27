"""Shared state passed between all LangGraph nodes."""
from typing import TypedDict


class JobState(TypedDict, total=False):
    job_description: str   # input from the user
    job_info: dict         # written by Node 1
    classification: dict   # written by Node 2
    top_skills: list       # written by Node 3
    report: dict           # written by Node 4
    error: str             # set if any node fails
