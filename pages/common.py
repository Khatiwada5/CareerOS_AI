from __future__ import annotations

from html import escape

import streamlit as st

from agents.profile_agent import get_current_profile
from agents.resume_agent import get_active_resume


def current_user_id() -> int | None:
    return st.session_state.get("user_id")


def page_title(title: str, caption: str = "") -> None:
    st.markdown(
        f"""
        <div class="page-hero">
          <div class="eyebrow">CareerOS AI</div>
          <h1>{escape(title)}</h1>
          <p>{escape(caption)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, caption: str = "") -> None:
    st.markdown(
        f"""
        <div class="section-heading">
          <h2>{escape(title)}</h2>
          <p>{escape(caption)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, body: str = "", accent: str = "blue") -> None:
    body_html = _markdownish_to_html(body)
    st.markdown(
        f"""
        <div class="cos-card cos-card-{accent}">
          <h3>{escape(title)}</h3>
          <div class="card-body">{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label: str, value: str, helper: str = "", tone: str = "blue") -> None:
    st.markdown(
        f"""
        <div class="metric-card metric-{tone}">
          <div class="label">{escape(label)}</div>
          <div class="value">{escape(str(value))}</div>
          <div class="helper">{escape(helper)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str) -> None:
    render_kpi_card(label, value)


def render_badge(text: str, tone: str = "blue") -> None:
    st.markdown(f'<span class="badge badge-{tone}">{escape(text)}</span>', unsafe_allow_html=True)


def render_skill_chip(skill: str, tone: str = "green") -> None:
    st.markdown(f'<span class="skill-chip chip-{tone}">{escape(skill)}</span>', unsafe_allow_html=True)


def render_skill_chips(skills: list[str], tone: str = "green", empty: str = "None detected yet") -> None:
    if not skills:
        st.caption(empty)
        return
    html = " ".join(f'<span class="skill-chip chip-{tone}">{escape(str(skill))}</span>' for skill in skills)
    st.markdown(f'<div class="chip-wrap">{html}</div>', unsafe_allow_html=True)


def render_score_bar(label: str, score: int | float, helper: str = "") -> None:
    safe_score = max(0, min(int(score or 0), 100))
    st.markdown(
        f"""
        <div class="score-card">
          <div class="score-top">
            <span>{escape(label)}</span>
            <strong>{safe_score}/100</strong>
          </div>
          <div class="score-track"><div class="score-fill" style="width:{safe_score}%"></div></div>
          <p>{escape(helper)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_warning_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="warning-card">
          <strong>{escape(title)}</strong>
          <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def recommendation_tone(recommendation: str) -> str:
    text = (recommendation or "").lower()
    if "strong" in text:
        return "green"
    if "apply" in text:
        return "blue"
    if "maybe" in text:
        return "yellow"
    return "red"


def show_ai_sections(text: str, fallback_title: str = "AI Output") -> None:
    sections = split_ai_sections(text)
    if not sections:
        render_card(fallback_title, text or "No output generated yet.")
        return
    for title, body in sections:
        render_card(title, body)


def split_ai_sections(text: str) -> list[tuple[str, str]]:
    content = (text or "").strip()
    if not content:
        return []
    lines = content.splitlines()
    sections: list[tuple[str, list[str]]] = []
    current_title = ""
    current_body: list[str] = []
    for line in lines:
        stripped = line.strip()
        is_heading = bool(stripped and stripped.endswith(":") and len(stripped) < 80 and not stripped.startswith("-"))
        if is_heading:
            if current_title or current_body:
                sections.append((current_title or "Details", current_body))
            current_title = stripped.rstrip(":")
            current_body = []
        else:
            current_body.append(line)
    if current_title or current_body:
        sections.append((current_title or "Details", current_body))
    return [(title, "\n".join(body).strip()) for title, body in sections if title or "".join(body).strip()]


def require_profile() -> dict | None:
    user_id = current_user_id()
    profile = get_current_profile(user_id)
    if not profile:
        render_warning_card("Profile needed", "Create your profile on the Home Dashboard first.")
        return None
    return profile


def latest_resume_text(user_id: int | None = None) -> str:
    resolved_user_id = user_id or current_user_id()
    if not resolved_user_id:
        return ""
    resume = get_active_resume(resolved_user_id)
    return resume.get("extracted_text", "") if resume else ""


def show_markdown_result(text: str) -> None:
    show_ai_sections(text)


def dataframe_or_empty(rows: list[dict], message: str) -> None:
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info(message)


def _markdownish_to_html(text: str) -> str:
    if not text:
        return ""
    html_parts: list[str] = []
    bullet_items: list[str] = []
    for raw_line in text.strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            bullet_items.append(f"<li>{escape(line[2:])}</li>")
            continue
        if bullet_items:
            html_parts.append(f"<ul>{''.join(bullet_items)}</ul>")
            bullet_items = []
        html_parts.append(f"<p>{escape(line)}</p>")
    if bullet_items:
        html_parts.append(f"<ul>{''.join(bullet_items)}</ul>")
    return "".join(html_parts)
