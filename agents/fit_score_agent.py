from __future__ import annotations

from backend.database import execute
from backend.utils import clean_text, detect_work_authorization_warning, extract_skills, score_to_recommendation, split_csv, top_keywords


def score_fit(user: dict, resume_text: str, job: dict) -> dict:
    profile_text = " ".join(
        str(user.get(field, "")) for field in ["school", "major", "target_roles", "skills", "experience", "projects", "career_goal"]
    )
    candidate_text = clean_text(f"{profile_text} {resume_text}").lower()
    job_text = clean_text(job.get("description", "")).lower()
    job_skills = set(job.get("skills") or extract_skills(job_text))
    candidate_skills = set(extract_skills(candidate_text)) | {s.lower() for s in split_csv(user.get("skills", ""))}

    matching_skills = sorted(skill for skill in job_skills if skill.lower() in candidate_skills or skill.lower() in candidate_text)
    missing_skills = sorted(skill for skill in job_skills if skill not in matching_skills)
    skill_score = round(40 * (len(matching_skills) / max(len(job_skills), 1)))

    exp_terms = ["intern", "project", "lead", "analy", "build", "develop", "research", "customer", "team"]
    experience_score = min(25, sum(3 for term in exp_terms if term in candidate_text and term in job_text))
    education_score = 15 if any(str(user.get(field, "")).lower() in job_text for field in ["major", "school"] if user.get(field)) else 8
    project_score = 10 if user.get("projects") and any(word in candidate_text for word in top_keywords(job_text, 8)) else 5
    job_keywords = set(top_keywords(job_text, 10))
    keyword_hits = [kw for kw in job_keywords if kw in candidate_text]
    keyword_score = round(10 * (len(keyword_hits) / max(len(job_keywords), 1)))

    total = max(0, min(100, skill_score + experience_score + education_score + project_score + keyword_score))
    recommendation = score_to_recommendation(total)
    warning = detect_work_authorization_warning(job_text)
    execute(
        """
        INSERT INTO job_analysis (user_id, company, role, job_description, fit_score, matching_skills, missing_skills, recommendation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user.get("id"),
            job.get("company", ""),
            job.get("role", ""),
            job.get("description", ""),
            total,
            ", ".join(matching_skills),
            ", ".join(missing_skills),
            recommendation,
        ),
    )
    return {
        "fit_score": total,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "experience_gaps": _experience_gaps(candidate_text, job_text),
        "visa_warning": warning,
        "recommendation": recommendation,
        "breakdown": {
            "skills_match": skill_score,
            "experience_match": experience_score,
            "education_match": education_score,
            "project_relevance": project_score,
            "keyword_match": keyword_score,
        },
    }


def _experience_gaps(candidate_text: str, job_text: str) -> list[str]:
    gaps = []
    for term in ["sql", "python", "customer", "dashboard", "machine learning", "stakeholder", "sales", "financial"]:
        if term in job_text and term not in candidate_text:
            gaps.append(term)
    return gaps[:6]
