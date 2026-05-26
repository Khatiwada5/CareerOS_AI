from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agents.cover_letter_agent import generate_cover_letter
from agents.fit_score_agent import score_fit
from agents.job_agent import parse_job_description
from agents.profile_agent import get_current_profile, upsert_profile
from agents.resume_agent import get_latest_resume
from agents.skill_gap_agent import create_skill_gap_plan
from agents.tailor_agent import tailor_resume
from backend.database import init_db

app = FastAPI(title="CareerOS AI API", version="0.1.0")


class ProfilePayload(BaseModel):
    name: str
    school: str = ""
    major: str = ""
    graduation_year: str = ""
    target_roles: str = ""
    skills: str = ""
    experience: str = ""
    projects: str = ""
    career_goal: str = ""


class JobPayload(BaseModel):
    company: str = ""
    role: str = ""
    job_description: str


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/profile")
def profile() -> dict:
    return get_current_profile() or {}


@app.post("/profile")
def save_profile(payload: ProfilePayload) -> dict:
    user_id = upsert_profile(payload.model_dump())
    return {"user_id": user_id}


@app.post("/job-fit")
def job_fit(payload: JobPayload) -> dict:
    current = get_current_profile() or {"id": 1}
    resume = get_latest_resume(current.get("id"))
    job = parse_job_description(payload.job_description, payload.company, payload.role)
    return score_fit(current, resume.get("extracted_text", "") if resume else "", job)


@app.post("/resume-tailor")
def resume_tailor(payload: JobPayload) -> dict:
    current = get_current_profile() or {}
    resume = get_latest_resume(current.get("id"))
    bullets = tailor_resume(current, resume.get("extracted_text", "") if resume else "", payload.job_description)
    return {"bullets": bullets}


@app.post("/cover-letter")
def cover_letter(payload: JobPayload) -> dict:
    current = get_current_profile() or {}
    letter = generate_cover_letter(current, payload.company, payload.role, payload.job_description)
    return {"cover_letter": letter}


@app.post("/skill-gap")
def skill_gap(payload: JobPayload) -> dict:
    current = get_current_profile() or {}
    return create_skill_gap_plan(current, payload.job_description)
