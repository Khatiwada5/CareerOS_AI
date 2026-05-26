from __future__ import annotations

import streamlit as st

from agents.graph import run_career_graph
from pages.common import page_title, render_card, render_section_header, require_profile


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
        render_section_header("Interview Prep Workspace", "Practice by category instead of reading one long answer.")
        behavioral, technical, business, recruiter = st.tabs(["Behavioral", "Technical/Role", "Business", "Questions to Ask Recruiter"])
        with behavioral:
            render_card("Behavioral Questions + STAR Answer", _pick_lines(result, ["tell me", "project", "team", "ambiguity", "STAR", "Situation"]), "blue")
        with technical:
            render_card("Technical / Role Questions", _pick_lines(result, ["technical", "decision", "skills", "role", "tool"]), "purple")
        with business:
            render_card("Business Judgment Prompts", _pick_lines(result, ["prioritize", "why this role", "why this company", "impact"]), "yellow")
        with recruiter:
            render_card("Questions To Ask Recruiter", _pick_lines(result, ["Questions to ask", "success", "90 days", "skills separate"]), "green")


def _pick_lines(text: str, keywords: list[str]) -> str:
    lines = [line for line in (text or "").splitlines() if line.strip()]
    selected = [line for line in lines if any(keyword.lower() in line.lower() for keyword in keywords)]
    return "\n".join(selected[:10]) or text
