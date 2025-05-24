from abc import ABC, abstractmethod
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv(override=False)


class AbstractDocumentSplitter(ABC):
    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        pass

    @abstractmethod
    def split_documents(self, documents: List[Document]) -> List[Document]:
        pass
