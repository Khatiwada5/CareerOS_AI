from __future__ import annotations

from backend.database import execute, fetch_all


def list_applications(user_id: int | None = None) -> list[dict]:
    if user_id:
        return fetch_all("SELECT * FROM applications WHERE user_id=? ORDER BY deadline IS NULL, deadline, id DESC", (user_id,))
    return fetch_all("SELECT * FROM applications ORDER BY deadline IS NULL, deadline, id DESC")


def add_application(user_id: int, data: dict) -> int:
    return execute(
        """
        INSERT INTO applications (user_id, company, role, job_link, date_applied, status, deadline, follow_up_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            data.get("company", ""),
            data.get("role", ""),
            data.get("job_link", ""),
            str(data.get("date_applied", "")),
            data.get("status", "Interested"),
            str(data.get("deadline", "")),
            str(data.get("follow_up_date", "")),
            data.get("notes", ""),
        ),
    )


def update_application(app_id: int, data: dict) -> None:
    execute(
        """
        UPDATE applications
        SET company=?, role=?, job_link=?, date_applied=?, status=?, deadline=?, follow_up_date=?, notes=?
        WHERE id=?
        """,
        (
            data.get("company", ""),
            data.get("role", ""),
            data.get("job_link", ""),
            str(data.get("date_applied", "")),
            data.get("status", "Interested"),
            str(data.get("deadline", "")),
            str(data.get("follow_up_date", "")),
            data.get("notes", ""),
            app_id,
        ),
    )


def delete_application(app_id: int) -> None:
    execute("DELETE FROM applications WHERE id=?", (app_id,))
