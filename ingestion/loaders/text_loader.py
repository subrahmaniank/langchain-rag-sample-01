from langchain_community.document_loaders import TextLoader
from document_loaders import AbstractDocumentLoader

class TextLoader (AbstractDocumentLoader):

    def load_document(self, file_path: str):
        loader = TextLoader(file_path)
        return loader.load()