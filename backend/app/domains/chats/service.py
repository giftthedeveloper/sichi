from __future__ import annotations

from typing import Optional

from app.domains.chats.intent_service import build_allowed_support_reply, build_escalation_reply, resolve_intent
from app.domains.chats.lookup_service import build_lookup_reply, run_lookup
from app.domains.chats import repository


def get_or_create_chat(profile_id: str, cursor: Optional[int], limit: int):
    chat = repository.get_or_create_active_chat(profile_id)
    messages, next_cursor, has_more = repository.list_messages(chat.id, cursor=cursor, limit=limit)
    return chat, messages, next_cursor, has_more


def get_chat_with_messages(chat_id: str, cursor: Optional[int], limit: int):
    chat = repository.get_chat(chat_id)
    messages, next_cursor, has_more = repository.list_messages(chat_id, cursor=cursor, limit=limit)
    return chat, messages, next_cursor, has_more


def send_message(chat_id: str, text: str):
    chat = repository.get_chat(chat_id)
    content = text.strip()
    repository.save_message(chat_id, "user", content)

    intent = resolve_intent(content)
    if not intent.is_allowed:
        repository.update_chat_state(chat_id, status="escalated", detail_stage=chat.detail_stage)
        try:
            reply = build_escalation_reply(content)
        except Exception:
            reply = "This issue is outside what I can resolve right now. I have escalated it to a human agent."
        repository.save_message(chat_id, "bot", reply)
    else:
        repository.update_chat_state(chat_id, status="active", detail_stage=chat.detail_stage + 1)
        try:
            lookup_result = run_lookup(profile_id=chat.profile_id, user_text=content)
            reply = build_lookup_reply(content, lookup_result)
        except Exception:
            try:
                reply = build_allowed_support_reply(content)
            except Exception:
                reply = "I am currently unavailable. Please try again shortly or reply with human for escalation."
        repository.save_message(chat_id, "bot", reply)

    latest_chat = repository.get_chat(chat_id)
    messages, next_cursor, has_more = repository.list_messages(chat_id, cursor=None, limit=20)
    return latest_chat, messages, next_cursor, has_more
