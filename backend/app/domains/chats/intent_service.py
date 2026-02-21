from __future__ import annotations

import json
from typing import Set

from app.domains.chats.config import get_all_categories, get_allowed_categories
from app.domains.chats.llm_client import ask_ollama

class IntentResult:
    def __init__(self, category: str, is_allowed: bool):
        self.category = category
        self.is_allowed = is_allowed


def classify_intent(text: str) -> str:
    categories = get_all_categories()
    system_prompt = (
        "You are a bank support intent classifier. "
        "Return ONLY JSON in this exact format: {\"category\":\"...\"}. "
        "Choose exactly one category from: "
        + ", ".join(categories)
    )
    try:
        raw = ask_ollama(prompt=text, system=system_prompt)
        parsed = json.loads(raw)
        category = str(parsed.get("category", "other")).strip()
        return category if category in categories else "other"
    except Exception:
        return "other"


def resolve_intent(text: str) -> IntentResult:
    category = classify_intent(text)
    allowed: Set[str] = get_allowed_categories()
    return IntentResult(category=category, is_allowed=category in allowed)


def build_allowed_support_reply(user_text: str) -> str:
    system_prompt = (
        "You are Sichi, a banking customer support assistant. "
        "Handle only banking transaction support in concise, practical language. "
        "If details are missing, ask one clear follow-up question."
    )
    return ask_ollama(prompt=user_text, system=system_prompt)


def build_escalation_reply(user_text: str) -> str:
    system_prompt = (
        "You are Sichi, a banking customer support assistant. "
        "Reply briefly that this issue is outside allowed scope and has been escalated to a human agent. "
        "Be polite and concise."
    )
    return ask_ollama(prompt=user_text, system=system_prompt)
