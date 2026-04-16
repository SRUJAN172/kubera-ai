from __future__ import annotations

from typing import Any, Dict
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def generate_explanation(prompt: str, model: str = MODEL_NAME) -> str:
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to connect to Ollama: {e}") from e

    data = response.json()
    text = data.get("response", "").strip()

    if not text:
        raise ValueError(f"Ollama returned an empty response: {data}")

    return text