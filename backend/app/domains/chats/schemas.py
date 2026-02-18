from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ChatStatus = Literal["active", "ready_to_resolve", "resolved", "escalated"]
Sender = Literal["user", "bot"]


class ChatSessionRequest(BaseModel):
    profile_id: str = Field(min_length=1, max_length=120)


class SendMessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class ChatMessageResponse(BaseModel):
    id: int
    sender: Sender
    text: str
    created_at: str


class ChatResponse(BaseModel):
    id: str
    profile_id: str
    status: ChatStatus
    detail_stage: int
    created_at: str
    updated_at: str
    messages: list[ChatMessageResponse]
    next_cursor: int | None
    has_more: bool
