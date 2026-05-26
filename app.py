from __future__ import annotations

import streamlit as st

from backend.database import init_db
from pages import (
    application_tracker,
    cover_letter,
    home,
    interview_prep,
    job_fit_scorer,
    resume_vault,
    resume_analyzer,
    resume_tailor,
    skill_gap,
)


st.set_page_config(page_title="CareerOS AI", page_icon="CO", layout="wide")
init_db()

PAGES = {
    "Home Dashboard": home.render,
    "Resume Vault": resume_vault.render,
    "Resume Analyzer": resume_analyzer.render,
    "Job Fit Scorer": job_fit_scorer.render,
    "Resume Tailor": resume_tailor.render,
    "Cover Letter Generator": cover_letter.render,
    "Interview Prep": interview_prep.render,
    "Skill Gap Planner": skill_gap.render,
    "Application Tracker": application_tracker.render,
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
          --primary: #2563eb;
          --ink: #172033;
          --muted: #667085;
          --panel: #ffffff;
          --line: #e6e8ee;
        }
        .main .block-container { padding-top: 1.6rem; max-width: 1180px; }
        h1, h2, h3 { color: var(--ink); letter-spacing: 0; }
        .metric-card {
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 18px;
          min-height: 112px;
          box-shadow: 0 1px 2px rgba(16, 24, 40, .04);
        }
        .metric-card .label { color: var(--muted); font-size: .86rem; }
        .metric-card .value { color: var(--ink); font-size: 1.9rem; font-weight: 700; margin-top: 6px; }
        .section-panel {
          background: #fff;
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 18px;
          margin-bottom: 14px;
        }
        .score-pill {
          display: inline-block;
          padding: 5px 10px;
          border-radius: 999px;
          background: #eef4ff;
          color: #174ea6;
          font-weight: 700;
        }
        div[data-testid="stSidebar"] { background: #f8fafc; }
        div.stButton > button {
          border-radius: 7px;
          border: 1px solid #cbd5e1;
          font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

with st.sidebar:
    st.title("CareerOS AI")
    st.caption("Career command center")
    selected_page = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("MVP mode: real LLM if an API key exists, otherwise mock career outputs.")

PAGES[selected_page]()
