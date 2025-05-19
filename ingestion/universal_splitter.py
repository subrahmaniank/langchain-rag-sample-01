import os

from ingestion.splitters.abstract_document_splitter import AbstractDocumentSplitter
from logging_config import setup_logger
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document
from ingestion.splitters import FixedWidthSplitter, SentenceSplitter, ParagraphSplitter, SemanticSplitter

logger = setup_logger(__name__)
load_dotenv()

# Initialize the abstract splitter as a reference
# splitter = AbstractDocumentSplitter()

class UniversalSplitter(AbstractDocumentSplitter):
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap


        # Get the chunking strategy from environment variable
        chunking_strategy = os.environ.get('CHUNKING_STRATEGY', 'fixed').lower()

        if chunking_strategy == 'fixed':
            self.splitter = FixedWidthSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
        elif chunking_strategy == 'sentence':
            self.splitter = SentenceSplitter()
        elif chunking_strategy == 'paragraph':
            self.splitter = ParagraphSplitter()
        elif chunking_strategy == 'semantic':
           self.splitter = SemanticSplitter()
        else:
            raise ValueError(f"Unknown chunking strategy: {chunking_strategy}")

    def split_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)

    def split_documents(self, documents: List[Document]) -> List[Document]:
        return self.splitter.split_documents(documents)

