import os

from langchain_experimental import text_splitter
from logging_config import setup_logger
from typing import List
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

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
            return self._fixed_size_chunking(text)
        elif chunking_strategy == 'sentence':
            return self._sentence_chunking(text)
        elif chunking_strategy == 'paragraph':
            return self._paragraph_chunking(text)
        else:
            raise ValueError(f"Unknown chunking strategy: {chunking_strategy}")

    def _fixed_size_chunking(self,text: str) -> List[str]:
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size

            # If this is not the first chunk, move the start back by the overlap amount
            if start > 0:
                start = start - self.overlap

            # If we're at the end of the text, just take what's left
            if end >= text_length:
                chunks.append(text[start:])
                break

            # Find the last space within the chunk to break on
            last_space = text.rfind(' ', start, end)

            if last_space != -1 and last_space > start:
                chunks.append(text[start:last_space])
                start = last_space + 1
            else:
                # If no space found, just break at the chunk size
                chunks.append(text[start:end])
                start = end

        return chunks

    def _sentence_chunking(self,text: str) -> List[str]:
        sentences = text.split('.')
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip() + '.'
            if current_length + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                overlap_words = ' '.join(current_chunk[-self.overlap:]).split()
                current_chunk = [word for word in overlap_words if isinstance(word, str)]
                current_length = sum(len(word) for word in overlap_words) + len(overlap_words) - 1

            current_chunk.append(sentence)
            current_length += len(sentence) + 1  # +1 for space

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def _paragraph_chunking(self,text: str) -> List[str]:
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_length = 0

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if current_length + len(paragraph) > self.chunk_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                overlap_paragraphs = current_chunk[-self.overlap:]
                current_chunk = overlap_paragraphs
                current_length = sum(len(p) for p in overlap_paragraphs) + 2 * (len(overlap_paragraphs) - 1)

            current_chunk.append(paragraph)
            current_length += len(paragraph) + 2  # +2 for newline characters

        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))

        return chunks


    def _semantic_chunking(self, text:str) -> List[str]:

        text_splitter = SemanticChunker(OpenAIEmbeddings(), breakpoint_threshold_type='percentile', breakpoint_threshold_amount=90, min_chunk_size=self.chunk_size)
        chunks = []
        chunks = text_splitter.create_documents([text])
        return chunks