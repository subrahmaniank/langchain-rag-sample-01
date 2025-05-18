from typing import List
from ingestion.splitters.abstract_document_splitter import AbstractDocumentSplitter
from langchain.schema import Document

class SentenceSplitter(AbstractDocumentSplitter):
    """Splits documents into chunks based on sentences (full stops)."""
    
    def __init__(self):
        super().__init__()

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split a list of documents into chunks based on sentences.
        
        Args:
            documents: List of Document objects to split
            
        Returns:
            List of Document objects split by sentences
        """
        split_docs = []
        
        for doc in documents:
            # Split content by full stops, preserving the full stop
            sentences = [s.strip() + '.' for s in doc.page_content.split('.') if s.strip()]
            
            # Create new Document for each sentence while preserving metadata
            for sentence in sentences:
                new_doc = Document(
                    page_content=sentence,
                    metadata=doc.metadata.copy()
                )
                split_docs.append(new_doc)
                
        return split_docs

    def split_text(self, text: str) -> List[str]:
        """
        Split a text string into chunks based on sentences.
        
        Args:
            text: String to split
            
        Returns:
            List of sentence strings
        """
        # Split by full stops and clean up
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        return sentences
