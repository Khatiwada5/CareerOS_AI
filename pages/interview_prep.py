from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import page_title, require_profile, show_markdown_result


def render() -> None:
    page_title("Interview Prep", "Generate likely questions, STAR examples, technical/business prompts, and recruiter questions.")
    profile = require_profile()
    if not profile:
        return
    role = st.text_input("Role")
    job_description = st.text_area("Role or job description", height=260)
    if st.button("Generate Interview Prep", type="primary"):
        result = run_career_graph(
            {
                "intent": "interview_prep",
                "profile": profile,
                "role": role,
                "job_description": job_description,
            }
        )
        show_markdown_result(result)
