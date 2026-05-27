from __future__ import annotations

import streamlit as st

from backend.auth import authenticate_user, create_user
from backend.database import init_db
from pages import (
    application_tracker,
    cover_letter,
    home,
    interview_prep,
    job_fit_scorer,
    profile,
    resume_vault,
    resume_analyzer,
    resume_tailor,
    skill_gap,
)


st.set_page_config(page_title="CareerOS AI", page_icon="CO", layout="wide")
init_db()

PAGES = {
    "Home Dashboard": home.render,
    "Profile": profile.render,
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
          --bg: #0a0f0d;
          --card: #111a15;
          --card-2: #1b4332;
          --blue: #2d6a4f;
          --purple: #1b4332;
          --green: #22C55E;
          --yellow: #FACC15;
          --red: #EF4444;
          --text: #F9FAFB;
          --muted: #9CA3AF;
          --line: rgba(148, 163, 184, .22);
        }
        .stApp {
          background:
            radial-gradient(circle at top left, rgba(59, 130, 246, .22), transparent 28rem),
            radial-gradient(circle at top right, rgba(45, 106, 79, .26), transparent 26rem),
            var(--bg);
          color: var(--text);
        }
        .main .block-container { padding-top: 1.4rem; max-width: 1220px; padding-bottom: 3rem; }
        h1, h2, h3, h4, p, label, span { letter-spacing: 0; }
        h1, h2, h3 { color: var(--text); }
        p, .stCaption, [data-testid="stMarkdownContainer"] { color: var(--muted); }
        .page-hero {
          border: 1px solid var(--line);
          border-radius: 22px;
          padding: 30px;
          margin-bottom: 24px;
          background: linear-gradient(135deg, rgba(45, 106, 79, .38), rgba(27, 67, 50, .32) 50%, rgba(17, 26, 21, .95));
          box-shadow: 0 24px 70px rgba(0, 0, 0, .28);
        }
        .page-hero .eyebrow {
          color: #B7E4C7;
          font-size: .78rem;
          text-transform: uppercase;
          font-weight: 800;
          letter-spacing: .1em;
          margin-bottom: 8px;
        }
        .page-hero h1 { font-size: 2.75rem; line-height: 1.05; margin: 0 0 10px; }
        .page-hero p { font-size: 1.05rem; margin: 0; color: #D1D5DB; max-width: 820px; }
        .section-heading { margin: 26px 0 12px; }
        .section-heading h2 { font-size: 1.15rem; margin-bottom: 2px; }
        .section-heading p { margin: 0; }
        .metric-card {
          background: linear-gradient(180deg, rgba(31, 41, 55, .9), rgba(17, 26, 21, .95));
          border: 1px solid var(--line);
          border-radius: 18px;
          padding: 18px;
          min-height: 124px;
          box-shadow: 0 16px 42px rgba(0, 0, 0, .2);
          position: relative;
          overflow: hidden;
        }
        .metric-card:before {
          content: "";
          position: absolute;
          inset: 0 auto 0 0;
          width: 4px;
          background: linear-gradient(var(--blue), var(--purple));
        }
        .metric-green:before { background: var(--green); }
        .metric-yellow:before { background: var(--yellow); }
        .metric-red:before { background: var(--red); }
        .metric-card .label { color: var(--muted); font-size: .82rem; font-weight: 700; text-transform: uppercase; }
        .metric-card .value { color: var(--text); font-size: 2rem; font-weight: 800; margin-top: 8px; }
        .metric-card .helper { color: var(--muted); font-size: .85rem; margin-top: 8px; }
        .cos-card, .section-panel, .score-card {
          background: rgba(17, 24, 39, .86);
          border: 1px solid var(--line);
          border-radius: 18px;
          padding: 18px 20px;
          margin-bottom: 16px;
          box-shadow: 0 18px 48px rgba(0, 0, 0, .18);
        }
        .cos-card h3 { font-size: 1rem; margin: 0 0 10px; }
        .cos-card .card-body { color: #D1D5DB; line-height: 1.6; }
        .cos-card ul { margin: 0; padding-left: 1.1rem; }
        .badge, .skill-chip {
          display: inline-flex;
          align-items: center;
          border-radius: 999px;
          padding: 6px 11px;
          font-size: .78rem;
          font-weight: 800;
          margin: 4px 6px 4px 0;
          border: 1px solid transparent;
        }
        .badge-blue, .chip-blue { background: rgba(45, 106, 79, .22); color: #B7E4C7; border-color: rgba(45, 106, 79, .48); }
        .badge-purple, .chip-purple { background: rgba(27, 67, 50, .32); color: #D8F3DC; border-color: rgba(27, 67, 50, .58); }
        .badge-green, .chip-green { background: rgba(34, 197, 94, .14); color: #BBF7D0; border-color: rgba(34, 197, 94, .35); }
        .badge-yellow, .chip-yellow { background: rgba(250, 204, 21, .14); color: #FEF08A; border-color: rgba(250, 204, 21, .38); }
        .badge-red, .chip-red { background: rgba(239, 68, 68, .15); color: #FECACA; border-color: rgba(239, 68, 68, .38); }
        .chip-wrap { margin: 8px 0 14px; }
        .score-top { display: flex; justify-content: space-between; align-items: center; color: var(--text); margin-bottom: 10px; }
        .score-top strong { font-size: 1.7rem; }
        .score-track { height: 12px; background: #273244; border-radius: 999px; overflow: hidden; }
        .score-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--blue), var(--purple)); }
        .score-card p { margin: 10px 0 0; }
        .warning-card {
          background: rgba(239, 68, 68, .12);
          border: 1px solid rgba(239, 68, 68, .34);
          border-radius: 16px;
          padding: 16px 18px;
          margin: 14px 0;
        }
        .warning-card strong { color: #FECACA; }
        .warning-card p { margin: 8px 0 0; color: #FCA5A5; }
        div[data-testid="stSidebar"] {
          background: linear-gradient(180deg, #111a15, #0a0f0d);
          border-right: 1px solid var(--line);
        }
        div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] span, div[data-testid="stSidebar"] label {
          color: var(--text);
        }
        div[data-testid="stSidebar"] .stRadio > div {
          gap: 7px;
        }
        div[data-testid="stSidebar"] [role="radiogroup"] label {
          background: rgba(31, 41, 55, .65);
          border: 1px solid rgba(148, 163, 184, .16);
          border-radius: 12px;
          padding: 8px 10px;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
          background: #111827;
          border-color: rgba(148, 163, 184, .28);
          color: var(--text);
        }
        div.stButton > button {
          border-radius: 12px;
          border: 1px solid rgba(59, 130, 246, .45);
          font-weight: 600;
          background: linear-gradient(135deg, #2d6a4f, #1b4332);
          color: white;
        }
        .stDataFrame {
          border: 1px solid var(--line);
          border-radius: 16px;
          overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

def render_auth_screen() -> None:
    page_col, form_col = st.columns([1.05, .95])
    with page_col:
        st.markdown(
            """
            <div class="page-hero">
              <div class="eyebrow">CareerOS AI</div>
              <h1>Own your career pipeline.</h1>
              <p>A private command center for resumes, job fit, interview prep, skill gaps, and applications.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with form_col:
        tab_login, tab_signup = st.tabs(["Login", "Sign up"])
        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login = st.form_submit_button("Login")
            if login:
                user = authenticate_user(username, password)
                if user:
                    st.session_state["user_id"] = user["id"]
                    st.session_state["username"] = user["username"] or user["name"]
                    st.toast("Logged in.", icon="✅")
                    st.rerun()
                st.error("Invalid username or password.")
        with tab_signup:
            with st.form("signup_form"):
                new_username = st.text_input("Choose username")
                new_password = st.text_input("Choose password", type="password")
                confirm_password = st.text_input("Confirm password", type="password")
                signup = st.form_submit_button("Create Account")
            if signup:
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                    return
                ok, message, user_id = create_user(new_username, new_password)
                if ok and user_id:
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = new_username.strip().lower()
                    st.toast("Account created.", icon="✅")
                    st.rerun()
                st.error(message)


if not st.session_state.get("user_id"):
    render_auth_screen()
    st.stop()

with st.sidebar:
    st.title("CareerOS AI")
    username = st.session_state.get("username", "user")
    st.markdown(f"### {username[:1].upper()}  `{username}`")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
    selected_page = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("Profile -> Resume Vault -> analyze, tailor, prep, and track.")

PAGES[selected_page]()
