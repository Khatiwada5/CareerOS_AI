from __future__ import annotations

import re

from backend.utils import extract_skills, top_keywords


def parse_job_description(job_description: str, company: str = "", role: str = "") -> dict:
    text = job_description or ""
    inferred_role = role or _infer_role(text)
    inferred_company = company or _infer_company(text)
    return {
        "company": inferred_company,
        "role": inferred_role,
        "skills": extract_skills(text),
        "keywords": top_keywords(text),
        "description": text,
    }


def _infer_role(text: str) -> str:
    match = re.search(r"(software engineer|data analyst|business analyst|product manager|marketing intern|finance intern|internship)", text, re.I)
    return match.group(1).title() if match else "Target Role"


def _infer_company(text: str) -> str:
    match = re.search(r"(?:at|company:)\s+([A-Z][A-Za-z0-9&.\s]{2,40})", text)
    return match.group(1).strip() if match else "Target Company"
