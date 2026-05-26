from __future__ import annotations

import streamlit as st

from agents.profile_agent import get_current_profile, upsert_profile
from agents.resume_agent import get_latest_resume
from agents.tracker_agent import list_applications
from backend.database import clear_all_data, fetch_all
from pages.common import (
    dataframe_or_empty,
    render_badge,
    render_card,
    render_kpi_card,
    render_score_bar,
    render_section_header,
    page_title,
)


def render() -> None:
    page_title(
        "CareerOS AI",
        "Your AI-powered career command center for resumes, job fit, interviews, skill gaps, and applications.",
    )

    profile = get_current_profile()
    applications = list_applications(profile["id"]) if profile else []
    latest_resume = get_latest_resume(profile["id"]) if profile else None
    analyses = fetch_all("SELECT company, role, fit_score, recommendation, created_at FROM job_analysis ORDER BY created_at DESC LIMIT 5")
    avg_score = round(sum(a["fit_score"] for a in analyses) / len(analyses), 1) if analyses else 0
    followups = [app for app in applications if app.get("follow_up_date")]
    resume_score = latest_resume.get("resume_score", 0) if latest_resume else 0
    interview_readiness = min(100, 35 + len(applications) * 8 + (20 if latest_resume else 0))
    skill_gap_risk = max(0, 100 - int(avg_score or 0)) if analyses else 55

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card("Resume Score", f"{resume_score}/100", "Latest saved resume", "blue")
    with col2:
        render_kpi_card("Average Job Fit", f"{avg_score}/100", "Across recent analyses", "green" if avg_score >= 75 else "yellow")
    with col3:
        render_kpi_card("Applications", str(len(applications)), "Tracked opportunities", "purple")
    with col4:
        render_kpi_card("Interview Ready", f"{interview_readiness}/100", "Profile + activity signal", "green")
    with col5:
        render_kpi_card("Skill Gap Risk", f"{skill_gap_risk}/100", "Lower is better", "red" if skill_gap_risk > 60 else "yellow")

    render_section_header("Recommended Next Actions", "A short path to make the demo and your workflow feel complete.")
    a1, a2, a3 = st.columns(3)
    with a1:
        render_card("1. Complete Profile", "Add school, major, target roles, projects, and skills so every agent has useful context.", "blue")
    with a2:
        render_card("2. Upload Resume", "Use Resume Vault to save a PDF or DOCX resume before scoring jobs or tailoring bullets.", "purple")
    with a3:
        render_card("3. Score A Target Role", "Paste a real job description to get a fit score, missing skills, and next steps.", "blue")

    render_section_header("Application Funnel", "A quick CRM-style snapshot of where your search stands.")
    if applications:
        _render_status_funnel(applications)
    else:
        render_card("No applications yet", "Add your first role in Application Tracker to activate the funnel and follow-up workflow.")

    with st.expander("Data Controls"):
        st.caption("Use this when you want to restart the demo with a blank profile, no saved resumes, no job analyses, and no applications.")
        confirm_clear = st.checkbox("I understand this will clear all saved app data")
        if st.button("Clear Form and Saved Data", disabled=not confirm_clear):
            clear_all_data()
            st.success("All saved data cleared. The form is ready for a fresh start.")
            st.rerun()

    render_section_header("Profile Setup", "This profile powers resume analysis, job fit scoring, letters, interview prep, and skill plans.")
    st.info("After saving your profile, go to Resume Vault to upload your PDF or DOCX resume once. The other tools will use your latest saved resume automatically.")
    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name", value=(profile or {}).get("name", ""))
            school = st.text_input("School", value=(profile or {}).get("school", ""))
            major = st.text_input("Major", value=(profile or {}).get("major", ""))
            graduation_year = st.text_input("Graduation year", value=(profile or {}).get("graduation_year", ""))
        with c2:
            target_roles = st.text_area("Target roles", value=(profile or {}).get("target_roles", ""), height=80)
            skills = st.text_area("Skills", value=(profile or {}).get("skills", ""), height=80)
        experience = st.text_area("Experience", value=(profile or {}).get("experience", ""), height=100)
        projects = st.text_area("Projects", value=(profile or {}).get("projects", ""), height=100)
        career_goal = st.text_area("Career goal", value=(profile or {}).get("career_goal", ""), height=80)
        submitted = st.form_submit_button("Save Profile")

    if submitted:
        upsert_profile(
            {
                "name": name,
                "school": school,
                "major": major,
                "graduation_year": graduation_year,
                "target_roles": target_roles,
                "skills": skills,
                "experience": experience,
                "projects": projects,
                "career_goal": career_goal,
            }
        )
        st.success("Profile saved.")
        st.rerun()

    render_section_header("Recent Activity", "Recent job analyses and follow-up reminders.")
    dataframe_or_empty(analyses, "No job analyses yet. Use Job Fit Scorer to create one.")

    render_section_header("Upcoming Follow-ups")
    if followups:
        st.dataframe(
            [
                {
                    "company": app.get("company"),
                    "role": app.get("role"),
                    "status": app.get("status"),
                    "follow_up_date": app.get("follow_up_date"),
                    "notes": app.get("notes"),
                }
                for app in followups
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No follow-up reminders saved yet.")


def _render_status_funnel(applications: list[dict]) -> None:
    counts = {}
    for app in applications:
        status = app.get("status") or "Interested"
        counts[status] = counts.get(status, 0) + 1
    max_count = max(counts.values()) if counts else 1
    for status, count in counts.items():
        width = int((count / max_count) * 100)
        st.markdown(
            f"""
            <div class="score-card">
              <div class="score-top"><span>{status}</span><strong>{count}</strong></div>
              <div class="score-track"><div class="score-fill" style="width:{width}%"></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
