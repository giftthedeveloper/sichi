from __future__ import annotations

from fastapi import APIRouter, Query

from app.domains.chats.models import Chat, ChatMessage
from app.domains.chats.schemas import ChatResponse, ChatMessageResponse, ChatSessionRequest, SendMessageRequest
from app.domains.chats import service

router = APIRouter(prefix="/chats", tags=["chats"])


def _message_to_schema(message: ChatMessage) -> ChatMessageResponse:
    return ChatMessageResponse(
        id=message.id,
        sender=message.sender,
        text=message.text,
        created_at=message.created_at,
    )


def _chat_to_schema(chat: Chat, messages: list[ChatMessage], next_cursor: int | None, has_more: bool) -> ChatResponse:
    return ChatResponse(
        id=chat.id,
        profile_id=chat.profile_id,
        status=chat.status,
        detail_stage=chat.detail_stage,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
        messages=[_message_to_schema(message) for message in messages],
        next_cursor=next_cursor,
        has_more=has_more,
    )


@router.post("/session", response_model=ChatResponse)
def get_or_create_chat_session(
    payload: ChatSessionRequest,
    cursor: int | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
) -> ChatResponse:
    chat, messages, next_cursor, has_more = service.get_or_create_chat(payload.profile_id, cursor=cursor, limit=limit)
    return _chat_to_schema(chat, messages, next_cursor, has_more)


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat_with_messages(
    chat_id: str,
    cursor: int | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
) -> ChatResponse:
    chat, messages, next_cursor, has_more = service.get_chat_with_messages(chat_id, cursor=cursor, limit=limit)
    return _chat_to_schema(chat, messages, next_cursor, has_more)


@router.post("/{chat_id}/messages", response_model=ChatResponse)
def send_chat_message(chat_id: str, payload: SendMessageRequest) -> ChatResponse:
    chat, messages, next_cursor, has_more = service.send_message(chat_id=chat_id, text=payload.text)
    return _chat_to_schema(chat, messages, next_cursor, has_more)
