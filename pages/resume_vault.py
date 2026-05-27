from __future__ import annotations

import streamlit as st

from agents.resume_agent import get_active_resume, list_resumes, remove_resume, save_resume, set_active_resume
from backend.resume_parser import extract_text_from_upload
from pages.common import dataframe_or_empty, page_title, render_card, render_score_bar, render_section_header, require_profile


def render() -> None:
    page_title("Resume Vault", "Upload and save your existing resume as a PDF, DOCX, or TXT file.")
    profile = require_profile()
    if not profile:
        return

    active = get_active_resume(profile["id"])
    if active:
        render_card("Active Resume", f"{active['file_name']}\nUploaded: {active['created_at']}", "green")
        render_score_bar("Active Resume Score", active.get("resume_score", 0), "Estimated from resume sections, skills, and measurable detail.")
        with st.expander("Preview extracted resume text"):
            st.text_area("Extracted text", value=active.get("extracted_text", ""), height=220, disabled=True)
    else:
        render_card("No Resume Saved Yet", "Upload one below so Job Fit Scorer, Resume Tailor, Cover Letter, Interview Prep, and Skill Gap Planner can use it.", "yellow")

    render_section_header("Upload Resume", "PDF, DOCX, and TXT files are supported.")
    uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
    if uploaded and st.button("Save Resume", type="primary"):
        try:
            text = extract_text_from_upload(uploaded)
            result = save_resume(profile["id"], uploaded.name, text)
            st.toast("Resume saved.", icon="✅")
            st.success(f"Saved {uploaded.name}. Estimated resume score: {result['resume_score']}/100")
            st.rerun()
        except Exception as exc:
            st.error(f"Could not save resume: {exc}")

    render_section_header("Saved Resumes")
    rows = [row for row in list_resumes() if row.get("user_id") == profile["id"]]
    if not rows:
        dataframe_or_empty(rows, "No resumes saved yet.")
        return
    for row in rows:
        with st.container():
            c1, c2, c3 = st.columns([2.2, .9, .9])
            with c1:
                active_label = "Active" if row.get("is_active") else "Saved"
                render_card(f"{active_label}: {row['file_name']}", f"Uploaded: {row['created_at']}\nScore: {row['resume_score']}/100", "green" if row.get("is_active") else "blue")
            with c2:
                if st.button("Set Active", key=f"active_{row['id']}", disabled=bool(row.get("is_active"))):
                    set_active_resume(profile["id"], row["id"])
                    st.toast("Active resume updated.", icon="✅")
                    st.rerun()
            with c3:
                confirm = st.checkbox("Confirm remove", key=f"confirm_resume_{row['id']}")
                if st.button("Remove Resume", key=f"remove_{row['id']}", disabled=not confirm):
                    remove_resume(profile["id"], row["id"])
                    st.toast("Resume removed.", icon="✅")
                    st.rerun()
