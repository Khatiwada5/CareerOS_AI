from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from backend.resume_parser import extract_text_from_upload
from pages.common import page_title, render_card, render_score_bar, render_section_header, render_skill_chips, require_profile, split_ai_sections


def render() -> None:
    page_title("Resume Analyzer", "Upload a resume and get a score, strengths, weaknesses, ATS tips, and better bullet ideas.")
    profile = require_profile()
    if not profile:
        return

    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
    if uploaded and st.button("Analyze Resume", type="primary"):
        try:
            with st.spinner("Analyzing resume with CareerOS AI..."):
                text = extract_text_from_upload(uploaded)
                result = run_career_graph(
                    {
                        "intent": "resume_analysis",
                        "profile": profile,
                        "file_name": uploaded.name,
                        "resume_text": text,
                    }
                )
            render_score_bar("Resume Score", result["resume_score"], "A quick ATS and content-readiness estimate.")
            render_section_header("Detected Skills", "Skills found in the uploaded resume.")
            render_skill_chips(result["skills"], "green", "No obvious skills detected yet.")
            render_section_header("Resume Feedback", "Organized into recruiter-friendly review areas.")
            sections = split_ai_sections(result["feedback"])
            for title, body in sections:
                tone = "blue"
                if "weak" in title.lower() or "missing" in title.lower():
                    tone = "yellow"
                if "ats" in title.lower():
                    with st.expander(title, expanded=True):
                        render_card("ATS Improvement Tips", body, "blue")
                else:
                    render_card(title, body, tone)
        except Exception as exc:
            st.error(f"Could not analyze resume: {exc}")
