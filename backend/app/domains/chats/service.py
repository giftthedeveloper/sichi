from __future__ import annotations

import asyncio
from time import perf_counter
from typing import Optional

from app.domains.chats.intent_service import (
    build_allowed_support_reply,
    build_neutral_redirect_reply,
    build_out_of_scope_reply,
    resolve_intent,
)
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


async def get_or_create_chat_async(profile_id: str, cursor: Optional[int], limit: int):
    return await asyncio.to_thread(get_or_create_chat, profile_id, cursor, limit)


async def get_chat_with_messages_async(chat_id: str, cursor: Optional[int], limit: int):
    return await asyncio.to_thread(get_chat_with_messages, chat_id, cursor, limit)


async def send_message(chat_id: str, text: str):
    started_total = perf_counter()
    chat = await asyncio.to_thread(repository.get_chat, chat_id)
    content = text.strip()
    await asyncio.to_thread(repository.save_message, chat_id, "user", content)

    t_intent = perf_counter()
    intent = await asyncio.to_thread(resolve_intent, content)
    intent_ms = (perf_counter() - t_intent) * 1000
    print(
        f"[sichi-timing] chat_send phase=intent chat_id={chat_id} "
        f"category={intent.category} route={intent.route} duration_ms={intent_ms:.1f}"
    )
    if intent.route == "allowed":
        await asyncio.to_thread(repository.update_chat_state, chat_id, "active", chat.detail_stage + 1)
        try:
            t_lookup = perf_counter()
            lookup_result = await asyncio.to_thread(run_lookup, chat.profile_id, content)
            lookup_ms = (perf_counter() - t_lookup) * 1000
            print(
                f"[sichi-timing] chat_send phase=lookup chat_id={chat_id} "
                f"action={lookup_result.action} duration_ms={lookup_ms:.1f}"
            )
            t_reply = perf_counter()
            reply = await asyncio.to_thread(build_lookup_reply, content, lookup_result)
            reply_ms = (perf_counter() - t_reply) * 1000
            print(f"[sichi-timing] chat_send phase=reply_lookup chat_id={chat_id} duration_ms={reply_ms:.1f}")
        except Exception:
            try:
                t_reply = perf_counter()
                reply = await asyncio.to_thread(build_allowed_support_reply, content)
                reply_ms = (perf_counter() - t_reply) * 1000
                print(f"[sichi-timing] chat_send phase=reply_fallback chat_id={chat_id} duration_ms={reply_ms:.1f}")
            except Exception:
                reply = "I am currently unavailable. Please try again shortly or reply with human for escalation."
        await asyncio.to_thread(repository.save_message, chat_id, "bot", reply)
    elif intent.route == "neutral":
        await asyncio.to_thread(repository.update_chat_state, chat_id, "active", chat.detail_stage)
        try:
            t_reply = perf_counter()
            reply = await asyncio.to_thread(build_neutral_redirect_reply, content)
            reply_ms = (perf_counter() - t_reply) * 1000
            print(f"[sichi-timing] chat_send phase=reply_neutral chat_id={chat_id} duration_ms={reply_ms:.1f}")
        except Exception:
            reply = "I am currently unavailable. Please try again shortly."
        await asyncio.to_thread(repository.save_message, chat_id, "bot", reply)
    else:
        await asyncio.to_thread(repository.update_chat_state, chat_id, "active", chat.detail_stage)
        try:
            t_reply = perf_counter()
            reply = await asyncio.to_thread(build_out_of_scope_reply, content)
            reply_ms = (perf_counter() - t_reply) * 1000
            print(f"[sichi-timing] chat_send phase=reply_out_of_scope chat_id={chat_id} duration_ms={reply_ms:.1f}")
        except Exception:
            reply = "I am currently unavailable. Please try again shortly."
        await asyncio.to_thread(repository.save_message, chat_id, "bot", reply)

    latest_chat = await asyncio.to_thread(repository.get_chat, chat_id)
    messages, next_cursor, has_more = await asyncio.to_thread(repository.list_messages, chat_id, None, 20)
    total_ms = (perf_counter() - started_total) * 1000
    print(f"[sichi-timing] chat_send phase=total chat_id={chat_id} duration_ms={total_ms:.1f}")
    return latest_chat, messages, next_cursor, has_more
