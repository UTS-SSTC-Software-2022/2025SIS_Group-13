from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import chromadb

#Retrieve
def retrieve(chromadb_collection, query: str, top_k: int) -> List[str]:
    query_embedding = embed_chunk(query)
    results = chromadb_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]

#Rerank
def rerank(query: str, retrieved_chunks: List[str], top_k: int) -> List[str]:
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    pairs = [(query, chunk) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    scored_chunks = list(zip(retrieved_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _ in scored_chunks][:top_k]

def prompt_building(query: str, chunks: List[str]) -> str:
    prompt = f"""You are a knowledge assistant. Please generate an accurate answer based on the user's question and the following chunks.

User Question: {query}

Relevant Chunks:
{"\n\n".join(chunks)}

Please answer strictly based on the above content. Do not fabricate information."""

    return prompt
