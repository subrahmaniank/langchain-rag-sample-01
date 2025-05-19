from typing import List
from ingestion.splitters.abstract_document_splitter import AbstractDocumentSplitter
from langchain.schema import Document

class FixedWidthSplitter(AbstractDocumentSplitter):
    """A document splitter that splits text into chunks of fixed width."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the fixed width splitter.
        
        Args:
            chunk_size (int): The size of each chunk in characters
            chunk_overlap (int): The number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """
        Split the input text into chunks of fixed width.
        
        Args:
            text (str): The input text to split
            
        Returns:
            List[str]: A list of text chunks
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            # Calculate end position for current chunk
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at a space
            if end < text_length:
                # Look for the last space within the chunk
                while end > start and text[end-1] != ' ':
                    end -= 1
                if end == start:  # No space found, force break at chunk_size
                    end = start + self.chunk_size

            # Add the chunk to our list
            chunks.append(text[start:end].strip())
            
            # Calculate the start of the next chunk considering overlap
            start = end - self.chunk_overlap if end < text_length else text_length

        return chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split multiple documents into chunks.
        
        Args:
            documents (List[Document]): List of Document objects to split
            
        Returns:
            List[Document]: A list of Document objects split into chunks
        """
        split_docs = []
        for doc in documents:
            # Split the document content
            text_chunks = self.split_text(doc.page_content)
            
            # Create new Document for each chunk while preserving metadata
            for chunk in text_chunks:
                new_doc = Document(
                    page_content=chunk,
                    metadata=doc.metadata.copy()
                )
                split_docs.append(new_doc)
                
        return split_docs
