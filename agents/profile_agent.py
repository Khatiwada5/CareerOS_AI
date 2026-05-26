from __future__ import annotations

from backend.database import execute, fetch_all, fetch_one


def upsert_profile(data: dict) -> int:
    existing = fetch_one("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    params = (
        data.get("name", "CareerOS User"),
        data.get("school", ""),
        data.get("major", ""),
        data.get("graduation_year", ""),
        data.get("target_roles", ""),
        data.get("skills", ""),
        data.get("experience", ""),
        data.get("projects", ""),
        data.get("career_goal", ""),
    )
    if existing:
        execute(
            """
            UPDATE users
            SET name=?, school=?, major=?, graduation_year=?, target_roles=?, skills=?, experience=?, projects=?, career_goal=?
            WHERE id=?
            """,
            (*params, existing["id"]),
        )
        return int(existing["id"])
    return execute(
        """
        INSERT INTO users (name, school, major, graduation_year, target_roles, skills, experience, projects, career_goal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        params,
    )


def get_current_profile() -> dict | None:
    return fetch_one("SELECT * FROM users ORDER BY id DESC LIMIT 1")


def list_profiles() -> list[dict]:
    return fetch_all("SELECT * FROM users ORDER BY id DESC")
