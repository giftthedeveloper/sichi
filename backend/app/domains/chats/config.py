from __future__ import annotations

import os
from typing import Set

DEFAULT_ALLOWED_CATEGORIES = {
    "failed_transfer",
    "card_debit_dispute",
    "bill_payment_issue",
    "reversal_request",
    "loan_request",
    "account_opening",
    "other",
}

DEFAULT_ALL_CATEGORIES = [
    "failed_transfer",
    "card_debit_dispute",
    "bill_payment_issue",
    "reversal_request",
    "loan_request",
    "account_opening",
    "other",
]


def _parse_csv_env(name: str) -> Set[str]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return set()
    values = set()
    for item in raw.split(","):
        value = item.strip()
        if value:
            values.add(value)
    return values


def get_ollama_url() -> str:
    return os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat").strip()


def get_ollama_model() -> str:
    return os.getenv("OLLAMA_MODEL", "mistral").strip()


def get_allowed_categories() -> Set[str]:
    configured = _parse_csv_env("ALLOWED_CATEGORIES")
    return configured if configured else set(DEFAULT_ALLOWED_CATEGORIES)


def get_all_categories() -> list[str]:
    configured = _parse_csv_env("ALL_CATEGORIES")
    if configured:
        return sorted(configured)
    return list(DEFAULT_ALL_CATEGORIES)
