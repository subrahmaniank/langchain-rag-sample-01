import os

from logging_config import setup_logger
from typing import List
from dotenv import load_dotenv
from ingestion.splitters import FixedWidthSplitter, SentenceSplitter, ParagraphSplitter, SemanticSplitter

logger = setup_logger(__name__)
load_dotenv()

class UniversalSplitter:
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        # Get the chunking strategy from environment variable
        chunking_strategy = os.environ.get('CHUNKING_STRATEGY', 'fixed').lower()

        if chunking_strategy == 'fixed':
            fixed_splitter = FixedWidthSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
            return fixed_splitter.split_text(text)
        elif chunking_strategy == 'sentence':
            sentence_splitter = SentenceSplitter()
            return sentence_splitter.split_text(text)
        elif chunking_strategy == 'paragraph':
            paragraph_splitter = ParagraphSplitter()
            return paragraph_splitter.split_text(text)
        elif chunking_strategy == 'semantic':
            semantic_splitter = SemanticSplitter()
            return semantic_splitter.split_text(text)
        else:
            raise ValueError(f"Unknown chunking strategy: {chunking_strategy}")
        
