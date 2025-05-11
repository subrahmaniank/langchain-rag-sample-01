import os
from urllib.parse import unquote
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from ingestion.loaders.abstract_document_loader import AbstractDocumentLoader
from logging_config import setup_logger

from dotenv import load_dotenv

logger = setup_logger(__name__)
load_dotenv()

class PDFLoader(AbstractDocumentLoader):
    """
    A class for loading and processing PDF documents.

    This class implements the AbstractDocumentLoader interface and provides
    methods to load PDF files, split them into chunks, and handle file paths.

    Attributes:
        file_path (str): The path to the PDF file to be loaded.
    """

    def __init__(self, file_path: str):
        """
        Initialize the PDFLoader with a file path.

        Args:
            file_path (str): The path to the PDF file.
        """
        self.file_path = file_path

    def _get_full_path(self) -> str:
        """
        Get the full absolute path of the PDF file.

        Returns:
            str: The full absolute path of the PDF file.
        """
        decoded_path = unquote(self.file_path)
        return os.path.abspath(os.path.expanduser(decoded_path))

    def load(self) -> List[Document]:
        """
        Load the PDF file and return a list of Document objects.

        Returns:
            List[Document]: A list of Document objects, each representing a page in the PDF.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            Exception: If there's an error while loading the PDF.
        """
        logger.debug(f"PDFLoader loading file: {self.file_path}")

        full_path = self._get_full_path()
        logger.debug(f"Full path: {full_path}")

        if not os.path.exists(full_path):
            logger.error(f"File does not exist at: {full_path}")
            raise FileNotFoundError(f"File not found: {full_path}")

        logger.info(f"File found at: {full_path}")

        try:
            loader = PyPDFLoader(full_path)
            documents = loader.load()
            logger.info(f"Successfully loaded {len(documents)} pages from the PDF.")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            raise

    def load_and_split(self) -> List[Document]:
        """
        Load the PDF file, split it into chunks, and return a list of Document objects.

        This method loads the PDF using the `load` method and then splits the
        resulting documents into smaller chunks using RecursiveCharacterTextSplitter.

        Returns:
            List[Document]: A list of Document objects representing chunks of the PDF content.
        """
        documents = self.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        split_docs = text_splitter.split_documents(documents)
        logger.info(f"Split documents into {len(split_docs)} chunks.")
        return split_docs

