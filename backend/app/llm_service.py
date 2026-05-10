from __future__ import annotations

from typing import Any, Dict
import requests

import os
from typing import Any, Dict
import requests

# Groq Config
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

# Ollama Config (Local Fallback)
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")


def generate_explanation(prompt: str) -> str:
    groq_api_key = os.environ.get("GROQ_API_KEY")

    if groq_api_key:
        # Use Groq API
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a strict financial analyst. Rules: Do not guess numbers. Be precise. Be concise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        }
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Groq API: {e}") from e
    else:
        # Fallback to Local Ollama
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"You are a strict financial analyst.\nRules:\n- Do not guess numbers\n- Be precise\n- Be concise\n\n{prompt}",
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()
            text = data.get("response", "").strip()
            if not text:
                return "Unable to generate explanation."
            return text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to connect to Ollama (Groq API key not found): {e}") from e


    

     
