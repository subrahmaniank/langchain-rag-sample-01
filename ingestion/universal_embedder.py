import os
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document

from common.embedders import BedrockEmbedder, OllamaEmbedder, OpenAIEmbedder
from common.embedders.abstract_document_embedder import AbstractDocumentEmbedder
from logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv(override=False)


class UniversalEmbedder(AbstractDocumentEmbedder):
    def __init__(self):

        # Get the chunking strategy from environment variable
        embedding_provider = os.environ.get(
            "EMBEDDING_MODEL_PROVIDER", "openai"
        ).lower()

        if embedding_provider == "openai":
            self.embedder = OpenAIEmbedder()
        elif embedding_provider == "ollama":
            self.embedder = OllamaEmbedder()
        elif embedding_provider == "aws":
            self.embedder = BedrockEmbedder()
        else:
            raise ValueError(f"Unknown embedding provider: {embedding_provider}")

    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        return self.embedder.embed_documents(documents)

    def embed_query(self, input_text: str) -> List[float]:
        return self.embedder.embed_query(input_text)
