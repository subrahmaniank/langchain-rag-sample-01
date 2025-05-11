from abc import ABC, abstractmethod

class AbstractDocumentLoader(ABC):
    @abstractmethod
    def load_document(self, file_path: str):
        pass