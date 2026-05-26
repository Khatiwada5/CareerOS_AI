from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from backend.resume_parser import extract_text_from_upload
from pages.common import page_title, require_profile, show_markdown_result


def render() -> None:
    page_title("Resume Analyzer", "Upload a resume and get a score, strengths, weaknesses, ATS tips, and better bullet ideas.")
    profile = require_profile()
    if not profile:
        return

    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
    if uploaded and st.button("Analyze Resume", type="primary"):
        try:
            text = extract_text_from_upload(uploaded)
            result = run_career_graph(
                {
                    "intent": "resume_analysis",
                    "profile": profile,
                    "file_name": uploaded.name,
                    "resume_text": text,
                }
            )
            st.metric("Resume Score", f"{result['resume_score']}/100")
            st.progress(result["resume_score"] / 100)
            st.write("Skills detected:", ", ".join(result["skills"]) or "No obvious skills detected")
            show_markdown_result(result["feedback"])
        except Exception as exc:
            st.error(f"Could not analyze resume: {exc}")
