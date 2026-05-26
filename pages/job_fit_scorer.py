from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import latest_resume_text, page_title, require_profile


def render() -> None:
    page_title("Job Fit Scorer", "Compare your profile and latest resume to a job description.")
    profile = require_profile()
    if not profile:
        return

    company = st.text_input("Company")
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
        st.metric("Fit Score", f"{result['fit_score']}/100", result["recommendation"])
        st.progress(result["fit_score"] / 100)
        st.subheader("Score Breakdown")
        st.json(result["breakdown"])
        c1, c2 = st.columns(2)
        with c1:
            st.write("Matching skills")
            st.success(", ".join(result["matching_skills"]) or "No direct matches found yet.")
        with c2:
            st.write("Missing skills")
            st.warning(", ".join(result["missing_skills"]) or "No major missing skills detected.")
        if result["experience_gaps"]:
            st.info("Experience gaps: " + ", ".join(result["experience_gaps"]))
        if result["visa_warning"]:
            st.error(result["visa_warning"])
