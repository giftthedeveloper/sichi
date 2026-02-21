from __future__ import annotations

from typing import Optional

from app.core.db import get_connection
from app.domains.profiles.models import Profile


def init_profiles_table() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
              id TEXT PRIMARY KEY,
              name TEXT NOT NULL
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_profiles_name ON profiles(name)")


def list_by_query(query: str) -> list[Profile]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name FROM profiles WHERE lower(name) LIKE ? ORDER BY name ASC LIMIT 20",
            (f"%{query.lower()}%",),
        ).fetchall()
    return [Profile(id=row["id"], name=row["name"]) for row in rows]


def create(name: str) -> Profile:
    clean_name = name.strip()
    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) AS total FROM profiles").fetchone()
        next_number = int(row["total"]) + 1 if row else 1
        profile_id = f"u-{next_number}"
        connection.execute(
            "INSERT INTO profiles (id, name) VALUES (?, ?)",
            (profile_id, clean_name),
        )
    return Profile(id=profile_id, name=clean_name)


def get_by_id(profile_id: str) -> Optional[Profile]:
    with get_connection() as connection:
        row = connection.execute("SELECT id, name FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    if not row:
        return None
    return Profile(id=row["id"], name=row["name"])
