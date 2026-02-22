from __future__ import annotations

import json
from typing import Set

from app.domains.chats.config import (
    get_all_categories,
    get_allowed_categories,
    get_neutral_categories,
    get_out_of_scope_categories,
)
from app.domains.chats.llm_client import ask_ollama
from app.domains.chats.policy_service import classifier_prompt, sichi_prompt


class IntentResult:
    def __init__(self, category: str, route: str):
        self.category = category
        self.route = route


def classify_intent(text: str) -> str:
    categories = get_all_categories()
    try:
        raw = ask_ollama(prompt=text, system=classifier_prompt(categories))
        parsed = json.loads(raw)
        category = str(parsed.get("category", "generic_help_request")).strip()
        return category if category in categories else "generic_help_request"
    except Exception:
        return "generic_help_request"


def resolve_intent(text: str) -> IntentResult:
    category = classify_intent(text)
    allowed: Set[str] = get_allowed_categories()
    neutral: Set[str] = get_neutral_categories()
    out_of_scope: Set[str] = get_out_of_scope_categories()
    if category in out_of_scope:
        return IntentResult(category=category, route="out_of_scope")
    if category in neutral:
        return IntentResult(category=category, route="neutral")
    if category in allowed:
        return IntentResult(category=category, route="allowed")
    return IntentResult(category=category, route="out_of_scope")


def build_allowed_support_reply(user_text: str) -> str:
    return ask_ollama(
        prompt=user_text,
        system=sichi_prompt(
            "Handle only banking transaction support in concise, practical language. "
            "If details are missing, ask one clear follow-up question."
        ),
    )


def build_neutral_redirect_reply(user_text: str) -> str:
    return ask_ollama(
        prompt=user_text,
        system=sichi_prompt(
            "The user has not stated a clear banking transaction issue yet. "
            "Reply politely, do not reveal any account or transaction data, and ask what banking transaction issue they need help with. "
            "Be concise."
        ),
    )


def build_out_of_scope_reply(user_text: str) -> str:
    return ask_ollama(
        prompt=user_text,
        system=sichi_prompt(
            "The user request is outside Sichi's primary function. "
            "Politely say you cannot help with that and that your primary function is banking transaction support only. "
            "Do not escalate. Be concise."
        ),
    )
