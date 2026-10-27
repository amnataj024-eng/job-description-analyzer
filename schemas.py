"""Pydantic models: the structured output of each LangGraph node."""
from typing import List, Literal
from pydantic import BaseModel, Field


class JobInfo(BaseModel):
    """Node 1 output: facts extracted from the job description."""
    job_title: str = Field(description="Job title, or 'Not specified'")
    company_name: str = Field(default="Not specified", description="Company name, or 'Not specified'")
    required_experience: str = Field(default="Not specified", description="e.g. '3+ years in backend development'")
    required_skills: List[str] = Field(default_factory=list, description="Short skill names, e.g. 'Python', 'SQL'")


class JobClassification(BaseModel):
    """Node 2 output: how the job should be categorised."""
    seniority_level: Literal["Intern", "Junior", "Mid-level", "Senior", "Lead/Principal", "Not specified"]
    job_category: str = Field(description="Broad domain, e.g. 'AI/ML Engineering', 'Backend Development'")
    reasoning: str = Field(description="One short sentence explaining the classification")


class TopSkill(BaseModel):
    rank: int
    skill: str
    reason: str = Field(description="Why this skill matters most for the role (one sentence)")


class TopSkills(BaseModel):
    """Node 3 output: the three most important skills."""
    top_skills: List[TopSkill] = Field(description="Exactly the 3 most important skills, ranked 1 to 3")


class HiringReport(BaseModel):
    """Node 4 output: the final structured hiring report."""
    job_title: str
    company_name: str
    required_experience: str
    required_skills: List[str]
    seniority_level: str
    job_category: str
    top_skills: List[TopSkill]
    summary: str
