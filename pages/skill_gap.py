from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import page_title, require_profile, show_markdown_result


def render() -> None:
    page_title("Skill Gap Planner", "Turn a target role into missing skills, a 30-day plan, resources, and portfolio ideas.")
    profile = require_profile()
    if not profile:
        return
    job_description = st.text_area("Target role or job description", height=280)
    if st.button("Create Skill Plan", type="primary"):
        result = run_career_graph(
            {
                "intent": "skill_gap",
                "profile": profile,
                "job_description": job_description,
            }
        )
        if result["missing_skills"]:
            st.write("Missing skills detected:", ", ".join(result["missing_skills"]))
        show_markdown_result(result["plan"])
