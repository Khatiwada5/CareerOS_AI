from __future__ import annotations

import streamlit as st

from agents.resume_agent import get_latest_resume, list_resumes, save_resume
from backend.resume_parser import extract_text_from_upload
from pages.common import dataframe_or_empty, page_title, require_profile


def render() -> None:
    page_title("Resume Vault", "Upload and save your existing resume as a PDF, DOCX, or TXT file.")
    profile = require_profile()
    if not profile:
        return

    latest = get_latest_resume(profile["id"])
    if latest:
        st.success(f"Latest saved resume: {latest['file_name']} ({latest['created_at']})")
        with st.expander("Preview extracted resume text"):
            st.text_area("Extracted text", value=latest.get("extracted_text", ""), height=220, disabled=True)
    else:
        st.info("No saved resume yet. Upload one below so the career tools can use it.")

    uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
    if uploaded and st.button("Save Resume", type="primary"):
        try:
            text = extract_text_from_upload(uploaded)
            result = save_resume(profile["id"], uploaded.name, text)
            st.success(f"Saved {uploaded.name}. Estimated resume score: {result['resume_score']}/100")
            st.rerun()
        except Exception as exc:
            st.error(f"Could not save resume: {exc}")

    st.subheader("Saved Resumes")
    rows = [row for row in list_resumes() if row.get("user_id") == profile["id"]]
    dataframe_or_empty(rows, "No resumes saved yet.")
