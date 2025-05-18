from typing import List
from ingestion.splitters.abstract_document_splitter import AbstractDocumentSplitter

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

    def split_documents(self, documents: List[str]) -> List[str]:
        """
        Split multiple documents into chunks.
        
        Args:
            documents (List[str]): List of documents to split
            
        Returns:
            List[str]: A list of text chunks from all documents
        """
        chunks = []
        for doc in documents:
            chunks.extend(self.split_text(doc))
        return chunks
