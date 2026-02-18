from __future__ import annotations

from app.domains.chats.models import Chat
from app.domains.chats import repository

HUMAN_TOKENS = ("human", "agent", "person", "staff")


def get_or_create_chat(profile_id: str, cursor: int | None, limit: int):
    chat = repository.get_or_create_active_chat(profile_id)
    messages, next_cursor, has_more = repository.list_messages(chat.id, cursor=cursor, limit=limit)
    return chat, messages, next_cursor, has_more


def get_chat_with_messages(chat_id: str, cursor: int | None, limit: int):
    chat = repository.get_chat(chat_id)
    messages, next_cursor, has_more = repository.list_messages(chat_id, cursor=cursor, limit=limit)
    return chat, messages, next_cursor, has_more


def send_message(chat_id: str, text: str):
    chat = repository.get_chat(chat_id)
    content = text.strip()
    repository.save_message(chat_id, "user", content)

    lowered = content.lower()
    if any(token in lowered for token in HUMAN_TOKENS):
        repository.update_chat_state(chat_id, status="escalated", detail_stage=chat.detail_stage)
        repository.save_message(chat_id, "bot", "Done. I have moved this chat to human support queue.")
    elif chat.status in ("resolved", "escalated"):
        repository.save_message(chat_id, "bot", "This chat is closed. Start a new chat for another issue.")
    elif chat.detail_stage == 0:
        repository.update_chat_state(chat_id, status="active", detail_stage=1)
        repository.save_message(chat_id, "bot", "Thanks. Please share transaction date and time.")
    elif chat.detail_stage == 1:
        repository.update_chat_state(chat_id, status="active", detail_stage=2)
        repository.save_message(chat_id, "bot", "Got it. Please provide transaction reference or recipient account.")
    elif chat.detail_stage == 2:
        repository.update_chat_state(chat_id, status="ready_to_resolve", detail_stage=3)
        repository.save_message(chat_id, "bot", f"Chat {chat_id} is complete. I can escalate to human support if needed.")
    else:
        repository.save_message(chat_id, "bot", 'Reply with "human" if you want escalation, or continue for more help.')

    latest_chat = repository.get_chat(chat_id)
    messages, next_cursor, has_more = repository.list_messages(chat_id, cursor=None, limit=20)
    return latest_chat, messages, next_cursor, has_more
