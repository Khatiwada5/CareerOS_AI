from __future__ import annotations

import bcrypt

from backend.database import execute, fetch_one


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_user(username: str, password: str) -> tuple[bool, str, int | None]:
    normalized = username.strip().lower()
    if len(normalized) < 3:
        return False, "Username must be at least 3 characters.", None
    if len(password) < 6:
        return False, "Password must be at least 6 characters.", None
    if fetch_one("SELECT id FROM users WHERE username=?", (normalized,)):
        return False, "That username is already taken.", None
    user_id = execute(
        """
        INSERT INTO users (username, password_hash, name, school, major, graduation_year, target_roles, skills, experience, projects, career_goal)
        VALUES (?, ?, ?, '', '', '', '', '', '', '', '')
        """,
        (normalized, hash_password(password), normalized),
    )
    return True, "Account created.", user_id


def authenticate_user(username: str, password: str) -> dict | None:
    normalized = username.strip().lower()
    user = fetch_one("SELECT * FROM users WHERE username=?", (normalized,))
    if user and verify_password(password, user.get("password_hash", "")):
        return user
    return None
