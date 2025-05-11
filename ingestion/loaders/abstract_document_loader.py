from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document


class AbstractDocumentLoader(ABC):
    @abstractmethod
    def load(self) -> List[Document]:
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
    def load_and_split(self) -> List[Document]:
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
