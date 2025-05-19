from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document


class AbstractDocumentSplitter(ABC):
    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        pass
    
    @abstractmethod
    def split_documents(self, documents: List[Document]) -> List[Document]:
        pass