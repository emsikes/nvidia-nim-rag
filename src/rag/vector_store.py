__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
from chromadb.config import Settings
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from typing import List, Dict
import os


class VectorStore:
    def __init__(self, collection_name="rag_documents"):
        """
        Instantiate a new instance of ChromaDB.  Disable anonymous usage reporting.  Allow resetting DB as needed.
        """
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = NVIDIAEmbeddings(
            model="nvidia/nv-embedqa-e5-v5",
            api_key=os.getenv("NVIDIA_API_KEY")
        )

    def add_documents(self, texts: List[str]):
        """
        Loop through input text and generate embeddings for each.  Then add them to our ChromaDB colllection.
        """
        embeddings = [self.embedder.embed_query(text) for text in texts]
        ids = [f"doc_{i}" for i in range(len(texts))]

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids
        )
        print(f"Added {len(texts)} documents to vector store")

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Embed the query, return the top 3 results by similarity search and return the matched docs in list form.
        """
        query_embedding = self.embedder.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results