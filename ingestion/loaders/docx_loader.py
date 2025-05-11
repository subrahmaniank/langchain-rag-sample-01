from langchain_community.document_loaders import UnstructedWordDocumentLoader
from document_loaders import AbstractDocumentLoader

class DocxLoader (AbstractDocumentLoader):

    def load_document(self, file_path: str):
        loader = UnstructuredWordDocumentLoader(file_path)
        return loader.load()