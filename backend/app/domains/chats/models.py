from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ChatStatus = Literal["active", "ready_to_resolve", "resolved", "escalated"]
Sender = Literal["user", "bot"]


@dataclass
class Chat:
    id: str
    profile_id: str
    status: ChatStatus
    detail_stage: int
    created_at: str
    updated_at: str


@dataclass
class ChatMessage:
    id: int
    chat_id: str
    sender: Sender
    text: str
    created_at: str
