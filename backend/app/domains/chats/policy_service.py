from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable


POLICY_PATH = Path(__file__).with_name("policy").joinpath("sichi_policy.md")


@lru_cache(maxsize=1)
def get_sichi_policy_text() -> str:
    try:
        return POLICY_PATH.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def with_policy(base_prompt: str) -> str:
    policy = get_sichi_policy_text()
    if not policy:
        return base_prompt
    return base_prompt + "\n\nPolicy:\n" + policy


def sichi_prompt(instruction: str) -> str:
    base = "You are Sichi, a banking customer support assistant. " + instruction.strip()
    return with_policy(base)


def classifier_prompt(categories: Iterable[str]) -> str:
    base = (
        "You are a bank support intent classifier. "
        "Return ONLY JSON in this exact format: {\"category\":\"...\"}. "
        "Choose exactly one category from: "
        + ", ".join(categories)
    )
    return with_policy(base)


def planner_prompt() -> str:
    base = (
        "You are an action planner for a banking bot. "
        "Return ONLY JSON in this format: "
        '{"action":"lookup_profile|lookup_transactions|lookup_balance|none","filters":{"transaction_id":"","state":"","type":"","account_last4":"","limit":5}}. '
        "Pick lookup_profile if user asks for name/profile/account identity. "
        "Pick lookup_transactions for transaction checks or references. "
        "Pick lookup_balance for balance questions."
    )
    return with_policy(base)
