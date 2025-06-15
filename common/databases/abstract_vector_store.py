from abc import ABC, abstractmethod
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv(override=False)


class AbstractVectorStore(ABC):
    @abstractmethod
    def save_doc_embeddings(
        self, documents: List[Document], embeddings: List[List[float]]
    ) -> None:
        pass

    def query_doc_embeddings(self, embeddings: List[float]) -> List[Document]:
        pass
