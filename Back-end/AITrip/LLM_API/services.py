# aiworker/services/gemini.py
import json
import os
import yaml
from typing import Any, Dict, Tuple
from django.conf import settings
from sentence_transformers import SentenceTransformer
import chromadb
import generation_processing as gp

# New unified SDK
from google import genai
from google.genai import types as genai_types

chromadb_client = chromadb.PersistentClient("./chroma.db")
chromadb_collection = chromadb_client.get_or_create_collection(name="default")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(BASE_DIR, "travel_assistant.yaml")

with open(yaml_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

system_prompt = config["system_prompt"]
response_schema = config["response_style"]["schema"]

# Create a single client (picks GEMINI_API_KEY from env automatically)
client = genai.Client(api_key=getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY'))
DEFAULT_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

def call_gemini(
    query: str,
    model_name: str | None = None,
    schema: dict | None = None,
    extra_config: dict | None = None,
) -> Tuple[Dict[str, Any], dict]:
    """Call Gemini and return (parsed_json, raw_dict_response). Ensures JSON output.


    - If `schema` is provided, we enable structured output.
    - We always request JSON mime type to make parsing robust.
    """
    model = model_name or DEFAULT_MODEL

    if schema:
        # Pass user-provided schema straight through
        config['response_schema'] = schema

    if extra_config:
        config.update(extra_config)

    # Prompt building with rag
    retrieved_chunks = gp.retrieve(chromadb_collection, query, 10)
    # for i, chunk in enumerate(retrieved_chunks):
    #     print(f"[{i}] {chunk}\n")
    reranked_chunks = gp.rerank(query, retrieved_chunks, 3)
    # for i, chunk in enumerate(reranked_chunks):
    #     print(f"[{i}] {chunk}\n")
    prompt = gp.prompt_building(query, reranked_chunks)
    
    # Compose contents; simplest is a single text part
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )

    # The SDK gives us .text as a JSON string. Parse defensively.
    text = getattr(response, 'text', '') or ''
    parsed: Dict[str, Any]
    try:
        parsed = json.loads(text)
    except Exception:
        # Fallback: return the raw text under a key so we never lose data
        parsed = {'raw_text': text}

    # Also provide the raw response as a dict for auditing
    raw_dict = getattr(response, 'to_dict', lambda: {})()

    return parsed, raw_dict

#!!!!!Need to know what front-end want to get!!!!!