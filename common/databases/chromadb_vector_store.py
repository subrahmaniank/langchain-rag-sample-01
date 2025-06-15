from abc import ABC, abstractmethod
import os
from typing import List
import uuid
import chromadb
from langchain.schema import Document

from common.databases.abstract_vector_store import AbstractVectorStore


class ChromadbVectorStore(AbstractVectorStore):

    def __init__(self) -> None:
        _database_file_path = os.environ.get("CHROMADB_FILE_PATH", "chromadb.sqlite")
        _collection_name = os.environ.get("CHROMADB_COLLECTION_NAME", "documents")

        _client = chromadb.PersistentClient(path=_database_file_path)
        _collection = _client.create_collection(_collection_name)
        self.collection = _collection

    def save_doc_embeddings(
        self, documents: List[Document], embeddings: List[List[float]]
    ) -> None:
        ids: List[str] = []
        docs: List[str] = []

        

        for document in documents:
            ids.append(str(uuid.uuid4()))


        self.collection.add(documents=docs, embeddings=embeddings, ids=ids)

    def query_doc_embeddings(self, embeddings: List[float]) -> List[Document]:
        pass
