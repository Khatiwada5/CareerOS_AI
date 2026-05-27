from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import page_title, render_badge, render_card, render_score_bar, render_section_header, render_skill_chips, require_profile, split_ai_sections


def render() -> None:
    page_title("Skill Gap Planner", "Turn a target role into missing skills, a 30-day plan, resources, and portfolio ideas.")
    profile = require_profile()
    if not profile:
        return
    job_description = st.text_area("Target role or job description", height=280)
    if st.button("Create Skill Plan", type="primary"):
        if not job_description.strip():
            st.error("Paste a target role or job description first.")
            return
        with st.spinner("Mapping skill gaps and learning plan..."):
            result = run_career_graph(
                {
                    "intent": "skill_gap",
                    "profile": profile,
                    "job_description": job_description,
                }
            )
        if result["missing_skills"]:
            render_section_header("Missing Skills", "Prioritize the highest-signal skills first.")
            render_skill_chips(result["missing_skills"], "yellow")
            for skill in result["missing_skills"][:5]:
                render_badge(f"{skill}: High priority", "red")
        risk = min(100, max(20, len(result["missing_skills"]) * 14))
        render_score_bar("Skill Gap Risk", risk, "Based on detected missing skills from the target role.")
        render_section_header("30-Day Skill Plan", "A practical path to close gaps and prove progress.")
        for title, body in split_ai_sections(result["plan"]):
            tone = "purple" if "project" in title.lower() else "blue"
            render_card(title, body, tone)
