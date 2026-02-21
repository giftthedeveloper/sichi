from __future__ import annotations

import json
from dataclasses import dataclass
import re

from app.domains.chats.llm_client import ask_ollama
from app.domains.profiles import service as profiles_service
from app.domains.transactions import repository as transactions_repository

ACTIONS = {"lookup_profile", "lookup_transactions", "lookup_balance", "none"}
GREETING_TERMS = {"hi", "hello", "heyy", "heyyy", "hey", "how", "far", "yo", "sup"}
BANKING_TERMS = {
    "transaction",
    "transfer",
    "debit",
    "credit",
    "balance",
    "account",
    "statement",
    "reversal",
    "card",
    "bills",
    "failed",
    "reference",
    "txn",
}


@dataclass
class LookupResult:
    action: str
    payload: dict[str, object]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _is_generic_message(user_text: str) -> bool:
    terms = _tokens(user_text)
    if not terms:
        return True
    if terms.intersection(BANKING_TERMS):
        return False
    return len(terms) <= 6 or bool(terms.intersection(GREETING_TERMS))


def _parse_action_json(raw: str) -> dict[str, object]:
    try:
        value = json.loads(raw)
    except Exception:
        return {"action": "none", "filters": {}}
    if not isinstance(value, dict):
        return {"action": "none", "filters": {}}
    action = str(value.get("action", "none"))
    filters = value.get("filters", {})
    if action not in ACTIONS:
        action = "none"
    if not isinstance(filters, dict):
        filters = {}
    return {"action": action, "filters": filters}


def _plan_action(user_text: str) -> dict[str, object]:
    if _is_generic_message(user_text):
        return {"action": "none", "filters": {}}
    system_prompt = (
        "You are an action planner for a banking bot. "
        "Return ONLY JSON in this format: "
        '{"action":"lookup_profile|lookup_transactions|lookup_balance|none","filters":{"transaction_id":"","state":"","type":"","account_last4":"","limit":5}}. '
        "Pick lookup_profile if user asks for name/profile/account identity. "
        "Pick lookup_transactions for transaction checks or references. "
        "Pick lookup_balance for balance questions."
    )
    raw = ask_ollama(prompt=user_text, system=system_prompt)
    return _parse_action_json(raw)


def _to_int(value: object, default: int, minimum: int, maximum: int) -> int:
    try:
        number = int(str(value))
    except Exception:
        return default
    return max(minimum, min(maximum, number))


def _execute_action(
    profile_id: str, action: str, filters: dict[str, object], user_text: str
) -> dict[str, object]:
    profile = profiles_service.get_profile(profile_id)
    if profile is None:
        return {"error": "profile_not_found"}

    if action == "lookup_profile":
        terms = _tokens(user_text)
        want_name = bool(terms.intersection({"name", "profile", "who"}))
        want_account = "account" in terms
        want_transaction = bool(terms.intersection({"transaction", "txn", "reference", "ref"}))
        if not (want_name or want_account or want_transaction):
            return {}
        latest = transactions_repository.list_for_profile(profile_name=profile.name, limit=1)
        latest_txn = latest[0] if latest else None
        payload: dict[str, object] = {"profile_id": profile.id}
        if want_name:
            payload["profile_name"] = profile.name
        if want_account:
            payload["latest_account_last4"] = latest_txn.account_last4 if latest_txn else ""
        if want_transaction:
            payload["latest_transaction_id"] = latest_txn.id if latest_txn else ""
        return payload

    if action == "lookup_balance":
        summary = transactions_repository.summarize_profile(profile.name)
        return {"profile_name": profile.name, "balance_summary": summary}

    if action == "lookup_transactions":
        limit = _to_int(filters.get("limit"), default=5, minimum=1, maximum=20)
        rows = transactions_repository.list_for_profile(
            profile_name=profile.name,
            limit=limit,
            transaction_id=str(filters.get("transaction_id", "")).strip(),
            state=str(filters.get("state", "")).strip(),
            transaction_type=str(filters.get("type", "")).strip(),
            account_last4=str(filters.get("account_last4", "")).strip(),
        )
        return {
            "profile_name": profile.name,
            "transactions": [
                {
                    "id": item.id,
                    "account_last4": item.account_last4,
                    "type": item.type,
                    "amount": item.amount,
                    "state": item.state,
                    "transaction_date": item.transaction_date,
                }
                for item in rows
            ],
        }

    return {}


def run_lookup(profile_id: str, user_text: str) -> LookupResult:
    action_data = _plan_action(user_text)
    action = str(action_data["action"])
    filters = action_data.get("filters", {})
    if not isinstance(filters, dict):
        filters = {}
    payload = _execute_action(profile_id=profile_id, action=action, filters=filters, user_text=user_text)
    return LookupResult(action=action, payload=payload)


def build_lookup_reply(user_text: str, lookup_result: LookupResult) -> str:
    system_prompt = (
        "You are Sichi, a banking customer support assistant. "
        "Use the lookup context to answer accurately and only reveal requested details. "
        "Do not invent data not present in context. "
        "If lookup action is none or payload is empty, do not reveal any account or transaction data. "
        "Instead ask a short follow-up question about what help the user needs. "
        "Keep reply concise in natural Nigerian English."
    )
    context = json.dumps({"action": lookup_result.action, "payload": lookup_result.payload})
    prompt = f"User message: {user_text}\nLookup context: {context}"
    return ask_ollama(prompt=prompt, system=system_prompt)
