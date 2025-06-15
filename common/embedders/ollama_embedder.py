import os
from typing import List
from langchain.schema import Document
from common.embedders.abstract_document_embedder import AbstractDocumentEmbedder
from logging_config import setup_logger
from langchain_ollama import OllamaEmbeddings

logger = setup_logger(__name__)


class OllamaEmbedder(AbstractDocumentEmbedder):
    def __init__(self):
        super().__init__()
        _embedding_model_provider = os.environ.get(
            "EMBEDDING_MODEL_PROVIDER", "OpenAI"
        ).lower()
        logger.debug(f"Using {_embedding_model_provider} embeddings")
        if _embedding_model_provider == "ollama":
            _ollama_base_url = os.environ.get(
                "OLLAMA_BASE_URL", "http://localhost:11434"
            )
            _ollama_embedding_model = os.environ.get(
                "EMBEDDING_MODEL_ID", "nomic-embed-text:latest"
            )
            _embedding_model = OllamaEmbeddings(
                base_url=_ollama_base_url, model=_ollama_embedding_model
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
