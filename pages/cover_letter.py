from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import page_title, require_profile, show_markdown_result


def render() -> None:
    page_title("Cover Letter Generator", "Create a concise, targeted cover letter that sounds human.")
    profile = require_profile()
    if not profile:
        return
    c1, c2 = st.columns(2)
    with c1:
        company = st.text_input("Company")
    with c2:
        role = st.text_input("Role")
    job_description = st.text_area("Job description", height=260)
    if st.button("Generate Cover Letter", type="primary"):
        result = run_career_graph(
            {
                "intent": "cover_letter",
                "profile": profile,
                "company": company,
                "role": role,
                "job_description": job_description,
            }
        )
        show_markdown_result(result)
