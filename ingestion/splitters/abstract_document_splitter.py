from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document


class AbstractDocumentSplitter(ABC):
    @abstractmethod
    def split(self, documents: List[Document]) -> List[Document]:
        """
        Split the input documents into smaller chunks.

        Args:
            documents (List[Document]): A list of documents to be split.

        Returns:
            List[Document]: A list of split documents.

        Raises:
            Exception: For any errors during the splitting process.
        """
        pass

    