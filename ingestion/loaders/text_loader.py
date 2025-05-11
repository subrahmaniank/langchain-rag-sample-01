import os
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import TextLoader as LangchainTextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ingestion.loaders.abstract_document_loader import AbstractDocumentLoader
from logging_config import setup_logger

logger = setup_logger(__name__)

class TextLoader(AbstractDocumentLoader):
    """
    A class for loading and processing text documents.

    This class implements the AbstractDocumentLoader interface and provides
    methods to load text files, split them into chunks, and handle file paths.

    Attributes:
        file_path (str): The path to the text file to be loaded.
    """

    def __init__(self, file_path: str):
        """
        Initialize the TextLoader with a file path.

        Args:
            file_path (str): The path to the text file.
        """
        self.file_path = file_path

    def _get_full_path(self) -> str:
        """
        Get the full absolute path of the text file.

        Returns:
            str: The full absolute path of the text file.
        """
        return os.path.abspath(os.path.expanduser(self.file_path))

    def load(self) -> List[Document]:
        """
        Load the text file and return a list of Document objects.

        Returns:
            List[Document]: A list of Document objects, typically containing one document for the entire text file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            Exception: If there's an error while loading the text file.
        """
        logger.debug(f"TextLoader loading file: {self.file_path}")
        
        full_path = self._get_full_path()
        logger.debug(f"Full path: {full_path}")
        
        if not os.path.exists(full_path):
            logger.error(f"File does not exist at: {full_path}")
            raise FileNotFoundError(f"File not found: {full_path}")
        
        logger.info(f"File found at: {full_path}")
        
        try:
            loader = LangchainTextLoader(full_path)
            documents = loader.load()
            logger.info(f"Successfully loaded text file with {len(documents)} document(s).")
            return documents
        except Exception as e:
            logger.error(f"Error loading text file: {str(e)}")
            raise

    def load_and_split(self) -> List[Document]:
        """
        Load the text file, split it into chunks, and return a list of Document objects.

        This method loads the text file using the `load` method and then splits the
        resulting documents into smaller chunks using RecursiveCharacterTextSplitter.

        Returns:
            List[Document]: A list of Document objects representing chunks of the text content.
        """
        documents = self.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(documents)
        logger.info(f"Split text document into {len(split_docs)} chunks.")
        return split_docs
