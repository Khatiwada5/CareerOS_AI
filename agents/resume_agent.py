from __future__ import annotations

from backend.database import execute, fetch_all, fetch_one
from backend.llm_client import LLMClient
from backend.utils import estimate_resume_score, extract_skills, top_keywords


def analyze_resume(user_id: int, file_name: str, extracted_text: str) -> dict:
    score = estimate_resume_score(extracted_text)
    feedback = LLMClient().generate(
        "resume_analysis",
        {
            "resume_text": extracted_text[:6000],
            "skills_found": extract_skills(extracted_text),
            "keywords": top_keywords(extracted_text),
        },
    )
    resume_id = execute(
        "INSERT INTO resumes (user_id, file_name, extracted_text, resume_score) VALUES (?, ?, ?, ?)",
        (user_id, file_name, extracted_text, score),
    )
    return {
        "resume_id": resume_id,
        "resume_score": score,
        "skills": extract_skills(extracted_text),
        "keywords": top_keywords(extracted_text),
        "feedback": feedback,
    }


def get_latest_resume(user_id: int | None = None) -> dict | None:
    if user_id:
        return fetch_one("SELECT * FROM resumes WHERE user_id=? ORDER BY created_at DESC, id DESC LIMIT 1", (user_id,))
    return fetch_one("SELECT * FROM resumes ORDER BY created_at DESC, id DESC LIMIT 1")


def list_resumes() -> list[dict]:
    return fetch_all("SELECT id, user_id, file_name, resume_score, created_at FROM resumes ORDER BY created_at DESC")
