from __future__ import annotations

from backend.llm_client import LLMClient


def generate_cover_letter(profile: dict, company: str, role: str, job_description: str) -> str:
    return LLMClient().generate(
        "cover_letter",
        {
            "name": profile.get("name", "Your Name"),
            "profile": profile,
            "company": company,
            "role": role,
            "job_description": job_description[:5000],
            "style": "Short, targeted, specific, early-career professional voice.",
        },
    )
