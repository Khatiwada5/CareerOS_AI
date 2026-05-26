from __future__ import annotations

from backend.llm_client import LLMClient


def generate_interview_prep(profile: dict, role: str, job_description: str) -> str:
    return LLMClient().generate(
        "interview_prep",
        {
            "profile": profile,
            "role": role,
            "job_description": job_description[:5000],
            "needs": "10 likely questions, sample answers, STAR behavioral answers, technical/business questions, recruiter questions.",
        },
    )
