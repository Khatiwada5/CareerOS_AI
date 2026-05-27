from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import page_title, render_card, render_section_header, require_profile


def render() -> None:
    page_title("Cover Letter Generator", "Create a concise, targeted cover letter that sounds human.")
    profile = require_profile()
    if not profile:
        return
    c1, c2 = st.columns([.9, 1.1])
    with c1:
        render_section_header("Writing Studio", "Enter role context and generate a concise letter.")
        company = st.text_input("Company")
        role = st.text_input("Role")
        job_description = st.text_area("Job description", height=300)
        generate = st.button("Generate Cover Letter", type="primary")
    with c2:
        render_section_header("Cover Letter Preview", "Short, targeted, and easy to copy into an application.")
        if generate:
            if not company.strip() or not role.strip() or not job_description.strip():
                st.error("Company, role, and job description are required.")
                return
            with st.spinner("Drafting a targeted cover letter..."):
                result = run_career_graph(
                    {
                        "intent": "cover_letter",
                        "profile": profile,
                        "company": company,
                        "role": role,
                        "job_description": job_description,
                    }
                )
            render_card(f"{role or 'Role'} at {company or 'Company'}", result, "purple")
        else:
            render_card("Preview", "Your generated cover letter will appear here after you add a company, role, and job description.", "blue")
