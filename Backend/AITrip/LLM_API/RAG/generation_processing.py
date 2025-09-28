import os
import yaml
from typing import List
from sentence_transformers import CrossEncoder
from . import preprocessing as pp

# Retrieve
def retrieve(chromadb_collection, query: str, top_k: int) -> List[str]:
    query_embedding = pp.embed_chunk_user(query)
    results = chromadb_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]

# Rerank
def rerank(query: str, retrieved_chunks: List[str], top_k: int) -> List[str]:
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    pairs = [(query, chunk) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    scored_chunks = list(zip(retrieved_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _ in scored_chunks][:top_k]

def load_yaml_config() -> dict:
    """Load the travel_assistant.yaml configuration."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(base_dir, "travel_assistant.yaml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def prompt_building(query: str, chunks: List[str]) -> str:
    config = load_yaml_config()
    system_prompt = config["system_prompt"]
    example_assistant = config["example_assistant"]

    prompt = f"""{system_prompt}

Please generate an accurate travel itinerary in strict JSON format.
The JSON MUST strictly follow the structure and field names in the example below.
Do not add extra text or explanations outside the JSON.

User Question (form input): {query}

Relevant Chunks:
{"\n\n".join(chunks)}

Expected JSON structure example:
{example_assistant}

If the chunks are empty or irrelevant, you may use your knowledge to generate a realistic itinerary,
but you MUST always return a valid JSON following the example schema.
"""

    return prompt
