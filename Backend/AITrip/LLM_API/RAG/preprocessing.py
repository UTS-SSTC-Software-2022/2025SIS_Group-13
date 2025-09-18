import os
from typing import List
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v2")

# split
def split_into_chunks(doc_file: str) -> List[str]:
    with open(doc_file, 'r', encoding='utf-8') as file:
        content = file.read()
    return [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]

# batch embedding
def embed_chunks(chunks: List[str]) -> List[List[float]]:
    return embedding_model.encode(chunks, normalize_embeddings=True).tolist()

def embed_chunk_user(chunk: str) -> List[float]:
    return embedding_model.encode(chunk, normalize_embeddings=True).tolist()

# save into Chroma
def save_embeddings(chromadb_collection, chunks: List[str], embeddings: List[List[float]], filename: str) -> None:
    chromadb_collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{filename}_{i}" for i in range(len(chunks))],
        metadatas=[{"filename": filename, "chunk_id": i} for i in range(len(chunks))]
    )

# log → split → embedding → Chroma
def process_and_store(chromadb_collection, dir_path: str):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)

        if os.path.isfile(file_path):
            chunks = split_into_chunks(file_path)
            if not chunks:
                continue

            embeddings = embed_chunks(chunks)
            save_embeddings(chromadb_collection, chunks, embeddings, filename)

    print("✅ All files stored into ChromaDB")

