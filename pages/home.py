from __future__ import annotations

import pandas as pd
import streamlit as st

from agents.profile_agent import get_current_profile, upsert_profile
from agents.tracker_agent import list_applications
from backend.database import fetch_all
from pages.common import dataframe_or_empty, metric_card, page_title


def render() -> None:
    page_title("CareerOS AI", "A practical career command center for resumes, roles, interviews, skill gaps, and applications.")

    profile = get_current_profile()
    applications = list_applications(profile["id"]) if profile else []
    analyses = fetch_all("SELECT company, role, fit_score, recommendation, created_at FROM job_analysis ORDER BY created_at DESC LIMIT 5")
    avg_score = round(sum(a["fit_score"] for a in analyses) / len(analyses), 1) if analyses else 0
    followups = [app for app in applications if app.get("follow_up_date")]

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Applications", str(len(applications)))
    with col2:
        metric_card("Average Fit Score", f"{avg_score}/100")
    with col3:
        metric_card("Upcoming Follow-ups", str(len(followups)))

    st.subheader("Profile Setup")
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

    st.subheader("Recent Job Analyses")
    dataframe_or_empty(analyses, "No job analyses yet. Use Job Fit Scorer to create one.")

    st.subheader("Upcoming Follow-ups")
    if followups:
        st.dataframe(pd.DataFrame(followups)[["company", "role", "status", "follow_up_date", "notes"]], use_container_width=True, hide_index=True)
    else:
        st.info("No follow-up reminders saved yet.")
