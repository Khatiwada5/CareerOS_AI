from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import latest_resume_text, page_title, render_card, render_section_header, render_skill_chips, require_profile


def render() -> None:
    page_title("Resume Tailor", "Generate stronger, honest, ATS-friendly bullets for a target role.")
    profile = require_profile()
    if not profile:
        return
    job_description = st.text_area("Job description", height=260)
    resume_text = st.text_area("Resume text override", value=latest_resume_text(profile["id"]), height=180)
    if st.button("Generate Tailored Bullets", type="primary"):
        if not job_description.strip():
            st.error("Paste a job description first.")
            return
        with st.spinner("Tailoring bullets without inventing experience..."):
            result = run_career_graph(
                {
                    "intent": "resume_tailor",
                    "profile": profile,
                    "resume_text": resume_text,
                    "job_description": job_description,
                }
            )
        render_section_header("Tailored Bullet Suggestions", "Use these as polished drafts, then edit them to match your real experience.")
        bullets = [line.strip("- ").strip() for line in result.splitlines() if line.strip().startswith("-")]
        if not bullets:
            bullets = [result]
        for index, bullet in enumerate(bullets, start=1):
            with st.container():
                render_card(f"Suggestion {index}", "")
                c1, c2 = st.columns(2)
                with c1:
                    render_card("Original Bullet", "Use one of your real existing bullets as the source before pasting this into your resume.", "yellow")
                with c2:
                    render_card("Improved Bullet", bullet, "green")
                render_card("Why It Works", "Stronger action verb, clearer scope, and role-relevant language without inventing experience.", "blue")
                keywords = [word for word in ["Python", "SQL", "dashboard", "analysis", "stakeholders", "automation", "documentation"] if word.lower() in bullet.lower()]
                render_skill_chips(keywords, "purple", "Keywords added will depend on your final edited bullet.")
