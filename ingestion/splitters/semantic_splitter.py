from typing import List, Optional
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from ingestion.splitters.abstract_document_splitter import AbstractDocumentSplitter

class SemanticSplitter(AbstractDocumentSplitter):
    """Split documents based on semantic similarity using embeddings."""

    def __init__(
        self,
        embeddings: Embeddings,
        chunk_size: int = 300,
        chunk_overlap: int = 50,
        threshold: float = 0.7,
    ):
        """Initialize semantic splitter.

        Args:
            embeddings: Embeddings model to use for semantic similarity
            chunk_size: Target size of chunks in characters
            chunk_overlap: Overlap between chunks in characters
            threshold: Similarity threshold for merging chunks
        """
        self.embeddings = embeddings
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.threshold = threshold
        self._semantic_chunker = SemanticChunker(
            embeddings=embeddings,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            threshold=threshold
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
