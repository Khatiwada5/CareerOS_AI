from __future__ import annotations

from backend.llm_client import LLMClient


def tailor_resume(profile: dict, resume_text: str, job_description: str) -> str:
    return LLMClient().generate(
        "resume_tailor",
        {
            "profile": profile,
            "resume_text": resume_text[:5000],
            "job_description": job_description[:5000],
            "rules": "Do not invent fake experience. Use stronger action verbs. Add metrics only when realistic. Keep bullets ATS-friendly.",
        },
    )
