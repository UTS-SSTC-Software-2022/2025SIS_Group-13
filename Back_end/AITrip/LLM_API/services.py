# aiworker/services/gemini.py
import os
import json
import yaml
from typing import Any, Dict, Tuple

# Initialize Django settings
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Back_end.AITrip.AITrip.settings")
django.setup()

from django.conf import settings
import chromadb
import Back_end.AITrip.LLM_API.RAG.generation_processing as gp

# New unified SDK
from google import genai
from google.genai import types as genai_types

# ---------- Helper functions ----------

def get_chromadb_collection():
    """Initialize or return the ChromaDB collection."""
    client = chromadb.PersistentClient("./chromaDB/chromaTest.db")
    return client.get_or_create_collection(name="default")


def get_gemini_client() -> genai.Client:
    """Initialize the Gemini client with API key from settings or environment."""
    api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in Django settings or environment variables")
    return genai.Client(api_key=api_key)


# ---------- Main function ----------

def call_gemini(
    query: str,
    model_name: str | None = None,
) -> Tuple[Dict[str, Any], dict]:
    """
    Call Gemini and return (parsed_json, raw_dict_response). Ensures JSON output.

    - If `schema` is provided, structured output is enabled.
    - Always request JSON mime type for parsing.
    """

    collection = get_chromadb_collection()
    client = get_gemini_client()
    model = model_name or os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

    # Retrieve and rerank chunks using RAG
    retrieved_chunks = gp.retrieve(collection, query, 10)
    reranked_chunks = gp.rerank(query, retrieved_chunks, 3)
    prompt = gp.prompt_building(query, reranked_chunks)

    # Generate response
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    # Parse JSON defensively
    text = getattr(response, 'text', '') or ''
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = {'raw_text': text}

    # Provide raw response dict for auditing
    raw_dict = getattr(response, 'to_dict', lambda: {})()

    return parsed, raw_dict
