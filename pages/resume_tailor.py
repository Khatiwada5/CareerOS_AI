from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import latest_resume_text, page_title, require_profile, show_markdown_result


def render() -> None:
    page_title("Resume Tailor", "Generate stronger, honest, ATS-friendly bullets for a target role.")
    profile = require_profile()
    if not profile:
        return
    job_description = st.text_area("Job description", height=260)
    resume_text = st.text_area("Resume text override", value=latest_resume_text(profile["id"]), height=180)
    if st.button("Generate Tailored Bullets", type="primary"):
        result = run_career_graph(
            {
                "intent": "resume_tailor",
                "profile": profile,
                "resume_text": resume_text,
                "job_description": job_description,
            }
        )
        show_markdown_result(result)
