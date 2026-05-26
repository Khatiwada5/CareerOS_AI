from __future__ import annotations

import streamlit as st

from agents.tracker_agent import add_application, delete_application, list_applications, update_application
from backend.models import APPLICATION_STATUSES
from pages.common import page_title, render_badge, render_card, render_kpi_card, render_section_header, require_profile


def render() -> None:
    page_title("Application Tracker", "Save applications, statuses, deadlines, follow-ups, and notes.")
    profile = require_profile()
    if not profile:
        return

    render_section_header("Add Application", "Capture the opportunity, status, deadline, follow-up date, and notes.")
    with st.form("add_application"):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            company = st.text_input("Company")
            role = st.text_input("Role")
            job_link = st.text_input("Job link")
        with c2:
            date_applied = st.date_input("Date applied")
            status = st.selectbox("Status", APPLICATION_STATUSES)
            deadline = st.date_input("Deadline")
        with c3:
            follow_up_date = st.date_input("Follow-up date")
            notes = st.text_area("Notes", height=124)
        submitted = st.form_submit_button("Add Application")

    if submitted:
        add_application(
            profile["id"],
            {
                "company": company,
                "role": role,
                "job_link": job_link,
                "date_applied": date_applied,
                "status": status,
                "deadline": deadline,
                "follow_up_date": follow_up_date,
                "notes": notes,
            },
        )
        st.success("Application added.")
        st.rerun()

    rows = list_applications(profile["id"])
    render_section_header("Application CRM", "Filter your pipeline and keep follow-ups visible.")
    if rows:
        status_filter = st.selectbox("Filter by status", ["All", *APPLICATION_STATUSES])
        filtered_rows = rows if status_filter == "All" else [row for row in rows if row.get("status") == status_filter]
        _render_tracker_summary(rows)
        st.dataframe(filtered_rows, use_container_width=True, hide_index=True)
        render_section_header("Status Badges")
        for status in APPLICATION_STATUSES:
            count = len([row for row in rows if row.get("status") == status])
            if count:
                render_badge(f"{status}: {count}", _status_tone(status))
        selected_id = st.selectbox("Select application to edit/delete", [row["id"] for row in rows], format_func=lambda app_id: _label_for(rows, app_id))
        selected = next(row for row in rows if row["id"] == selected_id)
        with st.form("edit_application"):
            c1, c2 = st.columns(2)
            with c1:
                e_company = st.text_input("Edit company", value=selected["company"])
                e_role = st.text_input("Edit role", value=selected["role"])
                e_job_link = st.text_input("Edit job link", value=selected["job_link"])
                e_date_applied = st.text_input("Edit date applied", value=selected["date_applied"])
            with c2:
                e_status = st.selectbox("Edit status", APPLICATION_STATUSES, index=APPLICATION_STATUSES.index(selected["status"]) if selected["status"] in APPLICATION_STATUSES else 0)
                e_deadline = st.text_input("Edit deadline", value=selected["deadline"])
                e_follow_up_date = st.text_input("Edit follow-up date", value=selected["follow_up_date"])
                e_notes = st.text_area("Edit notes", value=selected["notes"], height=96)
            update_clicked = st.form_submit_button("Update Application")
        if update_clicked:
            update_application(
                selected_id,
                {
                    "company": e_company,
                    "role": e_role,
                    "job_link": e_job_link,
                    "date_applied": e_date_applied,
                    "status": e_status,
                    "deadline": e_deadline,
                    "follow_up_date": e_follow_up_date,
                    "notes": e_notes,
                },
            )
            st.success("Application updated.")
            st.rerun()
        if st.button("Delete Selected Application"):
            delete_application(selected_id)
            st.warning("Application deleted.")
            st.rerun()
    else:
        st.info("No applications yet. Add your first opportunity above.")


def _label_for(rows: list[dict], app_id: int) -> str:
    row = next(item for item in rows if item["id"] == app_id)
    return f"{row['company']} - {row['role']}"


def _status_tone(status: str) -> str:
    return {
        "Interested": "blue",
        "Applied": "purple",
        "Interview": "green",
        "Rejected": "red",
        "Offer": "green",
    }.get(status, "blue")


def _render_tracker_summary(rows: list[dict]) -> None:
    c1, c2, c3, c4, c5 = st.columns(5)
    columns = [c1, c2, c3, c4, c5]
    for column, status in zip(columns, APPLICATION_STATUSES):
        count = len([row for row in rows if row.get("status") == status])
        with column:
            render_kpi_card(status, str(count), "pipeline count", _status_tone(status))
    max_count = max([len([row for row in rows if row.get("status") == status]) for status in APPLICATION_STATUSES] or [1])
    for status in APPLICATION_STATUSES:
        count = len([row for row in rows if row.get("status") == status])
        width = int((count / max(max_count, 1)) * 100)
        render_card(status, f"{count} application(s) in this stage\nPipeline share: {width}%", _status_tone(status))
