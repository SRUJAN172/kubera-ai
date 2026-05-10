from __future__ import annotations
import os
import json
from typing import Any, Dict
import requests

# Groq Config
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_VISION_MODEL = "llama-3.2-11b-vision-preview"

# Ollama Config (Local Fallback)
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
OLLAMA_VISION_MODEL = os.environ.get("OLLAMA_VISION_MODEL", "llama3.2-vision")

def generate_explanation(prompt: str) -> str:
    groq_api_key = os.environ.get("GROQ_API_KEY")

    if groq_api_key:
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
        except requests.exceptions.HTTPError as e:
            error_details = response.text
            raise RuntimeError(f"Failed to connect to Groq API (HTTP {response.status_code}): {error_details}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Groq API: {e}") from e
    else:
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

def analyze_receipt(base64_image: str, mime_type: str) -> dict:
    prompt = """
    You are a financial receipt analyzer. Extract the following details from this receipt and return ONLY a valid JSON object.
    Required JSON keys:
    - "amount": (float, the total amount charged)
    - "description": (string, the name of the store or merchant)
    - "date": (string, the date on the receipt in YYYY-MM-DD format, or today's date if not found)
    - "category": (string, choose ONE from: Food, Transport, Utilities, Entertainment, Health, Shopping, Others)
    
    Return EXACTLY a JSON object and nothing else. Do not wrap in markdown tags.
    """

    groq_api_key = os.environ.get("GROQ_API_KEY")

    if groq_api_key:
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            return json.loads(content)
        except Exception as e:
            raise RuntimeError(f"Failed to analyze receipt with Groq Vision: {e}") from e
    else:
        payload = {
            "model": OLLAMA_VISION_MODEL,
            "prompt": prompt,
            "images": [base64_image],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1}
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()
            text = data.get("response", "").strip()
            return json.loads(text)
        except Exception as e:
            raise RuntimeError(f"Failed to analyze receipt with Ollama Vision. Have you pulled the '{OLLAMA_VISION_MODEL}' model?: {e}") from e
