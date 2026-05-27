from __future__ import annotations

from backend.database import execute, fetch_all, fetch_one
from backend.llm_client import LLMClient
from backend.utils import estimate_resume_score, extract_skills, top_keywords


def save_resume(user_id: int, file_name: str, extracted_text: str) -> dict:
    score = estimate_resume_score(extracted_text)
    existing = fetch_one("SELECT id FROM resumes WHERE user_id=? LIMIT 1", (user_id,))
    is_active = 0 if existing else 1
    resume_id = execute(
        "INSERT INTO resumes (user_id, file_name, extracted_text, resume_score, is_active) VALUES (?, ?, ?, ?, ?)",
        (user_id, file_name, extracted_text, score, is_active),
    )
    return {
        "resume_id": resume_id,
        "resume_score": score,
        "skills": extract_skills(extracted_text),
        "keywords": top_keywords(extracted_text),
    }


def analyze_resume(user_id: int, file_name: str, extracted_text: str) -> dict:
    saved = save_resume(user_id, file_name, extracted_text)
    feedback = LLMClient().generate(
        "resume_analysis",
        {
            "resume_text": extracted_text[:6000],
            "skills_found": extract_skills(extracted_text),
            "keywords": top_keywords(extracted_text),
        },
    )
    return {
        **saved,
        "feedback": feedback,
    }


def get_latest_resume(user_id: int | None = None) -> dict | None:
    if user_id:
        return fetch_one("SELECT * FROM resumes WHERE user_id=? ORDER BY created_at DESC, id DESC LIMIT 1", (user_id,))
    return fetch_one("SELECT * FROM resumes ORDER BY created_at DESC, id DESC LIMIT 1")


def get_active_resume(user_id: int) -> dict | None:
    active = fetch_one("SELECT * FROM resumes WHERE user_id=? AND is_active=1 ORDER BY created_at DESC, id DESC LIMIT 1", (user_id,))
    return active or get_latest_resume(user_id)


def list_resumes() -> list[dict]:
    return fetch_all("SELECT id, user_id, file_name, resume_score, is_active, created_at FROM resumes ORDER BY created_at DESC")


def set_active_resume(user_id: int, resume_id: int) -> None:
    execute("UPDATE resumes SET is_active=0 WHERE user_id=?", (user_id,))
    execute("UPDATE resumes SET is_active=1 WHERE user_id=? AND id=?", (user_id, resume_id))


def remove_resume(user_id: int, resume_id: int) -> None:
    resume = fetch_one("SELECT is_active FROM resumes WHERE user_id=? AND id=?", (user_id, resume_id))
    execute("DELETE FROM resumes WHERE user_id=? AND id=?", (user_id, resume_id))
    if resume and resume.get("is_active"):
        latest = get_latest_resume(user_id)
        if latest:
            set_active_resume(user_id, latest["id"])
