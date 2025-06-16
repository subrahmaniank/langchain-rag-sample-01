import os
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document
from openai import vector_stores

from common.databases import ChromaDBVectorStore
from common.databases.abstract_vector_store import AbstractVectorStore
from logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv(override=False)


class UniversalVectorStore(AbstractVectorStore):
    def __init__(self):

        # Get the chunking strategy from environment variable
        vector_store = os.environ.get(
            "VECTOR_STORE", "chromadb"
        ).lower()

        if vector_store == "chromadb":
            self.vector_store = ChromaDBVectorStore()
        elif vector_store == "aws":
            self.vector_store = ChromaDBVectorStore()
        else:
            raise ValueError(f"Unknown vector store: {vector_store}")

    def save_doc_embeddings(
        self, documents: List[Document], embeddings: List[List[float]]
    ) -> None:
        return self.vector_store.save_doc_embeddings(documents, embeddings)

    def query_doc_embeddings(self, embeddings: List[float]) -> List[Document]:
        return self.vector_store.query_doc_embeddings(embeddings)
