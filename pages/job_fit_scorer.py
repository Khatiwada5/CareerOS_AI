from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import (
    latest_resume_text,
    page_title,
    recommendation_tone,
    render_badge,
    render_card,
    render_score_bar,
    render_section_header,
    render_skill_chips,
    render_warning_card,
    require_profile,
)


def render() -> None:
    page_title("Job Fit Scorer", "Compare your profile and latest resume to a job description.")
    profile = require_profile()
    if not profile:
        return

    c1, c2 = st.columns(2)
    with c1:
        company = st.text_input("Company")
    with c2:
        role = st.text_input("Role")
    job_description = st.text_area("Job description", height=260)
    resume_text = latest_resume_text(profile["id"])
    st.caption("Uses your saved profile and latest analyzed resume when available.")

    if st.button("Analyze Fit", type="primary"):
        result = run_career_graph(
            {
                "intent": "job_fit",
                "profile": profile,
                "company": company,
                "role": role,
                "job_description": job_description,
                "resume_text": resume_text,
            }
        )
        render_score_bar("Job Fit Score", result["fit_score"], "Weighted across skills, experience, education, projects, and keywords.")
        render_badge(result["recommendation"], recommendation_tone(result["recommendation"]))
        render_section_header("Score Breakdown")
        b1, b2, b3, b4, b5 = st.columns(5)
        breakdown = result["breakdown"]
        with b1:
            render_card("Skills", f"{breakdown['skills_match']}/40")
        with b2:
            render_card("Experience", f"{breakdown['experience_match']}/25")
        with b3:
            render_card("Education", f"{breakdown['education_match']}/15")
        with b4:
            render_card("Projects", f"{breakdown['project_relevance']}/10")
        with b5:
            render_card("Keywords", f"{breakdown['keyword_match']}/10")
        c1, c2 = st.columns(2)
        with c1:
            render_section_header("Matching Skills")
            render_skill_chips(result["matching_skills"], "green", "No direct matches found yet.")
        with c2:
            render_section_header("Missing Skills")
            render_skill_chips(result["missing_skills"], "yellow", "No major missing skills detected.")
        if result["experience_gaps"]:
            render_card("Experience Gaps", ", ".join(result["experience_gaps"]), "yellow")
        if result["visa_warning"]:
            render_warning_card("Work Authorization Check", result["visa_warning"])
        render_card(
            "Final Action Plan",
            "Tailor 2-3 resume bullets to the job description, add missing keywords truthfully, and prepare one project story that proves the top required skill.",
            "purple",
        )
