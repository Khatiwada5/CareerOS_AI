from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserProfile:
    name: str
    school: str = ""
    major: str = ""
    graduation_year: str = ""
    target_roles: str = ""
    skills: str = ""
    experience: str = ""
    projects: str = ""
    career_goal: str = ""


APPLICATION_STATUSES = ["Interested", "Applied", "Interview", "Rejected", "Offer"]
