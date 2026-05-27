from __future__ import annotations

import streamlit as st

from agents.profile_agent import upsert_profile
from backend.database import delete_user_account
from pages.common import page_title, render_section_header, render_warning_card, require_profile


def render() -> None:
    page_title("Profile", "Manage your private CareerOS profile and career context.")
    profile = require_profile()
    if not profile:
        return

    render_section_header("Career Profile", "These details power every AI workflow in CareerOS AI.")
    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name", value=profile.get("name", ""))
            school = st.text_input("School", value=profile.get("school", ""))
            major = st.text_input("Major", value=profile.get("major", ""))
            graduation_year = st.text_input("Graduation year", value=profile.get("graduation_year", ""))
        with c2:
            target_roles = st.text_area("Target roles", value=profile.get("target_roles", ""), height=90)
            skills = st.text_area("Skills", value=profile.get("skills", ""), height=90)
        experience = st.text_area("Experience", value=profile.get("experience", ""), height=110)
        projects = st.text_area("Projects", value=profile.get("projects", ""), height=110)
        career_goal = st.text_area("Career goal", value=profile.get("career_goal", ""), height=90)
        submitted = st.form_submit_button("Save Profile")

    if submitted:
        if not name.strip():
            st.error("Name is required.")
            return
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
            },
            profile["id"],
        )
        st.toast("Profile saved.", icon="✅")
        st.success("Profile saved.")
        st.rerun()

    render_section_header("Profile Controls", "Use confirmation steps for destructive actions.")
    clear_confirm = st.checkbox("Confirm clearing all profile form fields")
    if st.button("Clear Form", disabled=not clear_confirm):
        upsert_profile(
            {
                "name": profile.get("username", "CareerOS User"),
                "school": "",
                "major": "",
                "graduation_year": "",
                "target_roles": "",
                "skills": "",
                "experience": "",
                "projects": "",
                "career_goal": "",
            },
            profile["id"],
        )
        st.toast("Profile form cleared.", icon="✅")
        st.rerun()

    render_warning_card("Delete Profile", "This permanently deletes your account, resumes, applications, and analyses.")
    delete_confirm = st.checkbox("I understand this deletes my profile permanently")
    if st.button("Delete Profile", disabled=not delete_confirm):
        delete_user_account(profile["id"])
        st.session_state.clear()
        st.rerun()
