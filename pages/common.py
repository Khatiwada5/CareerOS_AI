from __future__ import annotations

import streamlit as st

from agents.profile_agent import get_current_profile
from agents.resume_agent import get_latest_resume


def page_title(title: str, caption: str = "") -> None:
    st.title(title)
    if caption:
        st.caption(caption)


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="label">{label}</div>
          <div class="value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def require_profile() -> dict | None:
    profile = get_current_profile()
    if not profile:
        st.warning("Create your profile on the Home Dashboard first.")
        return None
    return profile


def latest_resume_text(user_id: int | None = None) -> str:
    resume = get_latest_resume(user_id)
    return resume.get("extracted_text", "") if resume else ""


def show_markdown_result(text: str) -> None:
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown(text)
    st.markdown("</div>", unsafe_allow_html=True)


def dataframe_or_empty(rows: list[dict], message: str) -> None:
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info(message)
