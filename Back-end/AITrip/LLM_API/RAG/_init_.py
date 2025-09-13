#Process the knowledge datasets and store into chroma database

from sentence_transformers import SentenceTransformer
import chromadb
import preprocessing as pp

chromadb_client = chromadb.PersistentClient("./chroma.db")
chromadb_collection = chromadb_client.get_or_create_collection(name="default")

pp.process_and_store(chromadb_collection, "./docs")
