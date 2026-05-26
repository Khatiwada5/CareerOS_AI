from __future__ import annotations

import re
from collections import Counter


COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "sql", "excel", "tableau",
    "power bi", "pandas", "numpy", "react", "node", "fastapi", "flask",
    "django", "aws", "azure", "gcp", "docker", "kubernetes", "git",
    "machine learning", "data analysis", "statistics", "communication",
    "leadership", "project management", "figma", "salesforce", "seo",
    "marketing", "financial modeling", "accounting", "research", "testing",
}

ACTION_VERBS = [
    "Built", "Analyzed", "Designed", "Automated", "Led", "Improved",
    "Created", "Developed", "Optimized", "Collaborated", "Presented",
]


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def split_csv(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"[,;\n]", text or "") if item.strip()]


def extract_skills(text: str) -> list[str]:
    lowered = f" {clean_text(text).lower()} "
    found = [skill for skill in COMMON_SKILLS if f" {skill} " in lowered or skill in lowered]
    return sorted(set(found))


def top_keywords(text: str, limit: int = 12) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", (text or "").lower())
    stop = {
        "and", "the", "for", "with", "you", "our", "are", "will", "that",
        "this", "from", "have", "your", "role", "work", "team", "using",
    }
    counts = Counter(word for word in words if word not in stop)
    return [word for word, _ in counts.most_common(limit)]


def score_to_recommendation(score: int) -> str:
    if score >= 80:
        return "Strong Apply"
    if score >= 65:
        return "Apply with tailoring"
    if score >= 50:
        return "Maybe, needs improvement"
    return "Low fit"


def detect_work_authorization_warning(job_description: str) -> str:
    text = (job_description or "").lower()
    triggers = ["sponsorship", "work authorization", "authorized to work", "opt", "cpt", "f-1", "h-1b", "visa"]
    if any(trigger in text for trigger in triggers):
        return "This posting mentions sponsorship, visa, OPT/CPT, or work authorization. Review eligibility before applying."
    return ""


def estimate_resume_score(resume_text: str) -> int:
    text = (resume_text or "").lower()
    score = 35
    sections = ["education", "experience", "projects", "skills"]
    score += sum(10 for section in sections if section in text)
    score += min(len(extract_skills(text)) * 3, 15)
    score += 5 if re.search(r"\d+%|\$\d+|\d+\+|[0-9]+ users|[0-9]+ customers", text) else 0
    score += 5 if any(verb.lower() in text for verb in ACTION_VERBS) else 0
    return max(20, min(score, 100))
