#Process the knowledge datasets and store into chroma database
import os
import chromadb
#import .RAG.preprocessing as pp
from . import preprocessing as pp

chromadb_client = chromadb.PersistentClient("./chromaDB/chromaTest.db")
chromadb_collection = chromadb_client.get_or_create_collection(name="default")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
docs_path = os.path.join(BASE_DIR, "docs")
pp.process_and_store(chromadb_collection, docs_path)
