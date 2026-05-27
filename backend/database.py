from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / os.getenv("DATABASE_PATH", "data/careeros.db")


def ensure_data_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection():
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                name TEXT NOT NULL,
                school TEXT,
                major TEXT,
                graduation_year TEXT,
                target_roles TEXT,
                skills TEXT,
                experience TEXT,
                projects TEXT,
                career_goal TEXT
            );

            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                file_name TEXT,
                extracted_text TEXT,
                resume_score INTEGER,
                is_active INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                company TEXT,
                role TEXT,
                job_link TEXT,
                date_applied TEXT,
                status TEXT,
                deadline TEXT,
                follow_up_date TEXT,
                notes TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS job_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                company TEXT,
                role TEXT,
                job_description TEXT,
                fit_score INTEGER,
                matching_skills TEXT,
                missing_skills TEXT,
                recommendation TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )
        _ensure_column(conn, "users", "username", "TEXT")
        _ensure_column(conn, "users", "password_hash", "TEXT")
        _ensure_column(conn, "resumes", "is_active", "INTEGER DEFAULT 0")
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username)")


def fetch_all(query: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(query, tuple(params)).fetchall()
    return [dict(row) for row in rows]


def fetch_one(query: str, params: Iterable[Any] = ()) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(query, tuple(params)).fetchone()
    return dict(row) if row else None


def execute(query: str, params: Iterable[Any] = ()) -> int:
    with get_connection() as conn:
        cursor = conn.execute(query, tuple(params))
        return int(cursor.lastrowid)


def clear_all_data() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM job_analysis")
        conn.execute("DELETE FROM applications")
        conn.execute("DELETE FROM resumes")
        conn.execute("DELETE FROM users")


def clear_user_workspace(user_id: int, clear_profile: bool = False) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM job_analysis WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM applications WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM resumes WHERE user_id=?", (user_id,))
        if clear_profile:
            conn.execute(
                """
                UPDATE users
                SET name='', school='', major='', graduation_year='', target_roles='', skills='', experience='', projects='', career_goal=''
                WHERE id=?
                """,
                (user_id,),
            )


def delete_user_account(user_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM job_analysis WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM applications WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM resumes WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM users WHERE id=?", (user_id,))


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    columns = [row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
