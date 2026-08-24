import os
from typing import List, Dict

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


class HospitalRAG:
    
    def __init__(
        self,
        vector_db_path: str = None,
        collection_name: str = "hospital_documents"
    ):

        if vector_db_path is None:
            vector_db_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "..",
                    "vector_db"
                )
            )

        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.chroma_client = chromadb.PersistentClient(
            path=vector_db_path
        )

        self.collection = self.chroma_client.get_collection(
            name=collection_name
        )

        print(
            f"ChromaDB connected: "
            f"{self.collection.count()} documents"
        )

    # ---------------------------------------------------------
    # Create embedding
    # ---------------------------------------------------------

    def _create_embedding(self, text: str) -> List[float]:
        """
        Convert text into an embedding vector.
        """

        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    # ---------------------------------------------------------
    # Retrieve relevant documents
    # ---------------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve the most relevant hospital documents
        using ChromaDB vector similarity search.
        """

        if not query or not query.strip():
            return []

        # -----------------------------------------------------
        # Convert user question into embedding
        # -----------------------------------------------------

        query_embedding = self._create_embedding(query)

        # -----------------------------------------------------
        # Search ChromaDB
        # -----------------------------------------------------

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        retrieved_documents = []

        for i in range(len(documents)):

            metadata = metadatas[i] or {}

            retrieved_documents.append({
                "type": metadata.get("source", "unknown"),
                "id": ids[i],
                "title": "",
                "content": documents[i],
                "category": metadata.get(
                    "category",
                    "unknown"
                ),
                "score": round(
                    1 - float(distances[i]),
                    4
                )
            })

        return retrieved_documents

    # ---------------------------------------------------------
    # Build context for LLM
    # ---------------------------------------------------------

    def build_context(
        self,
        query: str,
        top_k: int = 5
    ) -> str:
        """
        Retrieve relevant documents and convert them
        into context that can be passed to the LLM.
        """

        results = self.retrieve(
            query=query,
            top_k=top_k
        )

        if not results:
            return "No relevant hospital information was found."

        context_parts = []

        for doc in results:

            context_parts.append(
                f"""
Source Type: {doc['type']}
Source ID: {doc['id']}
Category: {doc['category']}
Information: {doc['content']}
Relevance Score: {doc['score']}
""".strip()
            )

        return "\n\n---\n\n".join(context_parts)


# -------------------------------------------------------------
# Create reusable RAG instance
# -------------------------------------------------------------

rag = HospitalRAG()