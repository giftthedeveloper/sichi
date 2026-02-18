from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Tuple

from fastapi import HTTPException

from app.core.db import get_connection
from app.domains.chats.models import Chat, ChatMessage


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_chats_tables() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS chats (
              id TEXT PRIMARY KEY,
              profile_id TEXT NOT NULL,
              status TEXT NOT NULL,
              detail_stage INTEGER NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              chat_id TEXT NOT NULL,
              sender TEXT NOT NULL,
              text TEXT NOT NULL,
              created_at TEXT NOT NULL,
              FOREIGN KEY (chat_id) REFERENCES chats(id)
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_chats_profile ON chats(profile_id)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_messages_chat ON chat_messages(chat_id, id)")


def profile_exists(profile_id: str) -> bool:
    with get_connection() as connection:
        row = connection.execute("SELECT id FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    return row is not None


def get_or_create_active_chat(profile_id: str) -> Chat:
    if not profile_exists(profile_id):
        raise HTTPException(status_code=404, detail="Profile not found")
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, profile_id, status, detail_stage, created_at, updated_at
            FROM chats
            WHERE profile_id = ? AND status != 'resolved'
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (profile_id,),
        ).fetchone()
        if row:
            return Chat(**dict(row))

        count = connection.execute("SELECT COUNT(*) AS total FROM chats").fetchone()
        chat_id = f"CH-{(int(count['total']) if count else 0) + 1}"
        now = _now_iso()
        connection.execute(
            """
            INSERT INTO chats (id, profile_id, status, detail_stage, created_at, updated_at)
            VALUES (?, ?, 'active', 0, ?, ?)
            """,
            (chat_id, profile_id, now, now),
        )
    return Chat(id=chat_id, profile_id=profile_id, status="active", detail_stage=0, created_at=now, updated_at=now)


def get_chat(chat_id: str) -> Chat:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, profile_id, status, detail_stage, created_at, updated_at FROM chats WHERE id = ?",
            (chat_id,),
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Chat not found")
    return Chat(**dict(row))


def save_message(chat_id: str, sender: str, text: str) -> ChatMessage:
    now = _now_iso()
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO chat_messages (chat_id, sender, text, created_at) VALUES (?, ?, ?, ?)",
            (chat_id, sender, text.strip(), now),
        )
        connection.execute("UPDATE chats SET updated_at = ? WHERE id = ?", (now, chat_id))
        message_id = int(cursor.lastrowid)
    return ChatMessage(id=message_id, chat_id=chat_id, sender=sender, text=text.strip(), created_at=now)


def update_chat_state(chat_id: str, status: str, detail_stage: int) -> None:
    with get_connection() as connection:
        connection.execute(
            "UPDATE chats SET status = ?, detail_stage = ?, updated_at = ? WHERE id = ?",
            (status, detail_stage, _now_iso(), chat_id),
        )


def list_messages(
    chat_id: str, cursor: Optional[int], limit: int
) -> Tuple[list[ChatMessage], Optional[int], bool]:
    query = (
        "SELECT id, chat_id, sender, text, created_at FROM chat_messages "
        "WHERE chat_id = ? ORDER BY id DESC LIMIT ?"
    )
    params: tuple[object, ...] = (chat_id, limit + 1)
    if cursor is not None:
        query = (
            "SELECT id, chat_id, sender, text, created_at FROM chat_messages "
            "WHERE chat_id = ? AND id < ? ORDER BY id DESC LIMIT ?"
        )
        params = (chat_id, cursor, limit + 1)

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    has_more = len(rows) > limit
    trimmed = rows[:limit]
    messages_desc = [ChatMessage(**dict(row)) for row in trimmed]
    messages = list(reversed(messages_desc))
    next_cursor = messages_desc[-1].id if has_more and messages_desc else None
    return messages, next_cursor, has_more
