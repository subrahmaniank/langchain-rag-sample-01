from typing import List
from ingestion.splitters.abstract_document_splitter import AbstractDocumentSplitter

class ParagraphSplitter(AbstractDocumentSplitter):
    def __init__(self, min_length: int = 100, max_length: int = 1000):
        """Initialize the paragraph splitter with configurable length parameters.
        
        Args:
            min_length: Minimum length for a chunk
            max_length: Maximum length for a chunk
        """
        self.min_length = min_length
        self.max_length = max_length

    def split_text(self, text: str) -> List[str]:
        """Split text into paragraphs based on double newlines.
        
        Args:
            text: Input text to split
            
        Returns:
            List of text chunks split by paragraphs
        """
        # Split on double newlines to get paragraphs
        paragraphs = text.split('\n\n')
        
        # Clean and filter paragraphs
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            # Clean whitespace
            para = para.strip()
            if not para:
                continue
                
            para_length = len(para)
            
            # If paragraph exceeds max length, split it further
            if para_length > self.max_length:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_length = 0
                
                # Split long paragraph into sentences
                sentences = para.split('. ')
                for sentence in sentences:
                    if len(sentence) > self.max_length:
                        chunks.append(sentence[:self.max_length])
                    else:
                        chunks.append(sentence)
                        
            # Add to current chunk if within bounds
            elif current_length + para_length <= self.max_length:
                current_chunk.append(para)
                current_length += para_length
                
            # Start new chunk if adding would exceed max length
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [para]
                current_length = para_length
        
        # Add final chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        # Filter out chunks that are too small
        chunks = [chunk for chunk in chunks if len(chunk) >= self.min_length]
            
        return chunks

    def split_documents(self, documents: List[str]) -> List[str]:
        """Split multiple documents into chunks.
        
        Args:
            documents: List of document texts to split
            
        Returns:
            List of text chunks from all documents
        """
        chunks = []
        for doc in documents:
            chunks.extend(self.split_text(doc))
        return chunks
