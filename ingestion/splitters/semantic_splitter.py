import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

from ingestion.splitters.abstract_document_splitter import AbstractDocumentSplitter
from logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv(override=False)


class SemanticSplitter(AbstractDocumentSplitter):
    """Split documents based on semantic similarity using embeddings."""

    def __init__(
        self,
    ):
        """Initialize semantic splitter.

        Args:
            chunk_size: Target size of chunks in characters
            chunk_overlap: Overlap between chunks in characters
            threshold: Similarity threshold for merging chunks
        """
        _embedding_model_provider = os.environ.get(
            "SCS_EMBEDDING_MODEL_PROVIDER", "OpenAI"
        ).lower()
        logger.debug(f"Using {_embedding_model_provider} embeddings")
        if _embedding_model_provider == "ollama":
            _ollama_base_url = os.environ.get(
                "SCS_OLLAMA_BASE_URL", "http://localhost:11434"
            )
            _ollama_embedding_model = os.environ.get(
                "SCS_OLLAMA_EMBEDDING_MODEL", "nomic-embed-text:latest"
            )
            _embedding_model = OllamaEmbeddings(
                base_url=_ollama_base_url,
                model=_ollama_embedding_model,
            )
        else:
            _embedding_model = OpenAIEmbeddings()

        _min_chunk_size = os.environ.get("SCS_MIN_CHUNK_SIZE", None)
        _breakpoint_threshold_type = os.environ.get(
            "SCS_BREAKPOINT_THRESHOLD_TYPE", "percentile"
        ).lower()

        self._semantic_chunker = SemanticChunker(
            embeddings=_embedding_model,
            min_chunk_size=(
                int(_min_chunk_size) if _min_chunk_size is not None else None
            ),
            breakpoint_threshold_type=(
                "gradient"
                if _breakpoint_threshold_type == "gradient"
                else (
                    "standard_deviation"
                    if _breakpoint_threshold_type == "standard_deviation"
                    else (
                        "percentile"
                        if _breakpoint_threshold_type == "percentile"
                        else "interquartile"
                    )
                )
            ),
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into semantically coherent chunks.

        Args:
            documents: List of documents to split

        Returns:
            List of split documents
        """
        all_splits = []
        for doc in documents:
            splits = self._semantic_chunker.split_text(doc.page_content)
            for split in splits:
                metadata = doc.metadata.copy()
                all_splits.append(Document(page_content=split, metadata=metadata))
        return all_splits

    def split_text(self, text: str) -> List[str]:
        """Split text into semantically coherent chunks.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        return self._semantic_chunker.split_text(text)

    def create_documents(
        self, texts: List[str], metadatas: Optional[List[dict]] = None
    ) -> List[Document]:
        """Create documents from texts with optional metadata.

        Args:
            texts: List of texts to convert to documents
            metadatas: Optional list of metadata dicts

        Returns:
            List of documents
        """
        _metadatas = metadatas or [{}] * len(texts)
        documents = [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, _metadatas)
        ]
        return self.split_documents(documents)
