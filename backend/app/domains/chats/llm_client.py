from __future__ import annotations

from time import perf_counter
from typing import Any, Dict

import requests

from app.domains.chats.config import get_ollama_model, get_ollama_url


def ask_ollama(prompt: str, system: str, timeout_seconds: int = 30, trace: str = "ollama") -> str:
    started = perf_counter()
    model = get_ollama_model()
    url = get_ollama_url()
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {"temperature": 0.1},
    }
    try:
        response = requests.post(url, json=payload, timeout=timeout_seconds)
        response.raise_for_status()
        data = response.json()
        message = data.get("message", {})
        content = message.get("content", "")
        elapsed_ms = (perf_counter() - started) * 1000
        print(f"[sichi-timing] ollama_call trace={trace} model={model} status=ok duration_ms={elapsed_ms:.1f}")
        return str(content).strip()
    except Exception as exc:
        elapsed_ms = (perf_counter() - started) * 1000
        print(f"[sichi-timing] ollama_call trace={trace} model={model} status=error duration_ms={elapsed_ms:.1f}")
        raise RuntimeError("Local Ollama request failed") from exc
