import os
from typing import List

from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings

from common.embedders.abstract_document_embedder import AbstractDocumentEmbedder
from logging_config import setup_logger


logger = setup_logger(__name__)


class OpenAIEmbedder(AbstractDocumentEmbedder):
    def __init__(self):
        _embedding_model_provider = os.environ.get(
            "EMBEDDING_MODEL_PROVIDER", "OpenAI"
        ).lower()
        logger.debug(f"Using {_embedding_model_provider} embeddings")

        if _embedding_model_provider != "openai":
            raise ValueError(f"{_embedding_model_provider} is not supported")

        _openai_embedding_model = os.environ.get(
            "EMBEDDING_MODEL_ID", "nomic-embed-text:latest"
        )
        _embedding_model = OpenAIEmbeddings(
            model=_openai_embedding_model,
        )
        self._embedding_model = _embedding_model

    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        # iterate through the document List
        doc_content: List[str] = []
        for document in documents:
            doc_content.append(document.page_content)
        vectors = self._embedding_model.embed_documents(doc_content)
        return vectors

    def embed_query(self, input_text: str) -> List[float]:
        vectors = self._embedding_model.embed_query(input_text)
        return vectors
