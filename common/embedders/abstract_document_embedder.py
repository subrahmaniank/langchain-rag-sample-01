from abc import ABC, abstractmethod
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv(override=False)


class AbstractDocumentEmbedder(ABC):
    @abstractmethod
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """
        Load the document and return a list of Document objects.

        Returns:
            List[Document]: A list of loaded documents.

        Raises:
            FileNotFoundError: If the file is not found.
            PermissionError: If there's no permission to read the file.
            Exception: For any other errors during loading.
        """
        pass

    @abstractmethod
    def embed_query(self, input_text: str) -> List[float]:
        """
        Load the document, split it into chunks, and return a list of Document objects.

        Returns:
            List[Document]: A list of loaded and split documents.

        Raises:
            FileNotFoundError: If the file is not found.
            PermissionError: If there's no permission to read the file.
            Exception: For any other errors during loading or splitting.
        """
        pass
