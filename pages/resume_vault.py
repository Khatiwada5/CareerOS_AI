from __future__ import annotations

import streamlit as st

from agents.resume_agent import get_latest_resume, list_resumes, save_resume
from backend.resume_parser import extract_text_from_upload
from pages.common import dataframe_or_empty, page_title, render_card, render_score_bar, render_section_header, require_profile


def render() -> None:
    page_title("Resume Vault", "Upload and save your existing resume as a PDF, DOCX, or TXT file.")
    profile = require_profile()
    if not profile:
        return

    latest = get_latest_resume(profile["id"])
    if latest:
        render_card("Latest Saved Resume", f"{latest['file_name']}\nSaved: {latest['created_at']}", "green")
        render_score_bar("Resume Vault Score", latest.get("resume_score", 0), "Estimated from resume sections, skills, and measurable detail.")
        with st.expander("Preview extracted resume text"):
            st.text_area("Extracted text", value=latest.get("extracted_text", ""), height=220, disabled=True)
    else:
        render_card("No Resume Saved Yet", "Upload one below so Job Fit Scorer, Resume Tailor, Cover Letter, Interview Prep, and Skill Gap Planner can use it.", "yellow")

    render_section_header("Upload Resume", "PDF, DOCX, and TXT files are supported.")
    uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
    if uploaded and st.button("Save Resume", type="primary"):
        try:
            text = extract_text_from_upload(uploaded)
            result = save_resume(profile["id"], uploaded.name, text)
            st.success(f"Saved {uploaded.name}. Estimated resume score: {result['resume_score']}/100")
            st.rerun()
        except Exception as exc:
            st.error(f"Could not save resume: {exc}")

    render_section_header("Saved Resumes")
    rows = [row for row in list_resumes() if row.get("user_id") == profile["id"]]
    dataframe_or_empty(rows, "No resumes saved yet.")
