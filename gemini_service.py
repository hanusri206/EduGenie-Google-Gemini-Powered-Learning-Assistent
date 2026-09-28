import json
import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


_client = None


def get_client():

    global _client

    if _client is not None:
        return _client

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please create a .env file and add your Gemini API key."
        )

    try:
        from google import genai

    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install -r requirements.txt"
        ) from exc

    _client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return _client


def generate_text(
    prompt: str,
    temperature: float = 0.4
) -> str:

    client = get_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


def generate_json(
    prompt: str,
    schema: dict[str, Any]
) -> Any:

    client = get_client()

    try:
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is not installed."
        ) from exc

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema
        )
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty JSON response."
        )

    try:
        return json.loads(text)

    except json.JSONDecodeError as exc:

        cleaned = clean_json_block(text)

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            ) from exc


def clean_json_block(text: str) -> str:

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()