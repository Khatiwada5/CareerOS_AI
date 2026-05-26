from __future__ import annotations

from backend.llm_client import LLMClient
from backend.utils import extract_skills, split_csv


def create_skill_gap_plan(profile: dict, job_description: str) -> dict:
    candidate_skills = {skill.lower() for skill in split_csv(profile.get("skills", ""))}
    job_skills = set(extract_skills(job_description))
    missing = sorted(skill for skill in job_skills if skill.lower() not in candidate_skills)
    plan = LLMClient().generate(
        "skill_gap",
        {
            "profile": profile,
            "job_description": job_description[:5000],
            "missing_skills": missing,
        },
    )
    return {"missing_skills": missing, "plan": plan}
