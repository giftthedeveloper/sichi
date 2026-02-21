from __future__ import annotations

from typing import Any, Dict

import requests

from app.domains.chats.config import get_ollama_model, get_ollama_url


def ask_ollama(prompt: str, system: str, timeout_seconds: int = 30) -> str:
    payload: Dict[str, Any] = {
        "model": get_ollama_model(),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {"temperature": 0.1},
    }
    try:
        response = requests.post(get_ollama_url(), json=payload, timeout=timeout_seconds)
        response.raise_for_status()
        data = response.json()
        message = data.get("message", {})
        content = message.get("content", "")
        return str(content).strip()
    except Exception as exc:
        raise RuntimeError("Local Ollama request failed") from exc
