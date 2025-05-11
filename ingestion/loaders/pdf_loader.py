from langchain_community.document_loaders import PyPDFLoader
from abstract_document_loader import AbstractDocumentLoader

class PDFLoader (AbstractDocumentLoader):

    def load_document(self, file_path: str):
        loader = PyPDFLoader(file_path)
        return loader.load()