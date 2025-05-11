import os
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ingestion.loaders.abstract_document_loader import AbstractDocumentLoader
from logging_config import setup_logger

logger = setup_logger(__name__)

class DocxLoader(AbstractDocumentLoader):
    def __init__(self, file_path: str):
        """
        Initialize the DocxLoader with the path to the DOCX file.

        Args:
            file_path (str): The path to the DOCX file to be loaded.

        Example:
            >>> loader = DocxLoader("/path/to/your/docx/file.docx")
        """
        self.file_path = file_path

    def _get_full_path(self) -> str:
        """
        Get the absolute path of the file.

        This method expands the user directory (if present) and converts the
        file path to an absolute path.

        Returns:
            str: The absolute path of the file.

        Example:
            >>> loader = DocxLoader("~/Documents/sample.docx")
            >>> loader._get_full_path()
            '/home/user/Documents/sample.docx'
        """
        return os.path.abspath(os.path.expanduser(self.file_path))

    def load(self) -> List[Document]:
        """
        Load the DOCX file and return a list of Document objects.

        This method reads the DOCX file from the specified path, converts it
        into a list of Document objects, and returns the list.

        Returns:
            List[Document]: A list of Document objects loaded from the DOCX file.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
            Exception: For any other errors during loading.

        Example:
            >>> loader = DocxLoader("/path/to/your/docx/file.docx")
            >>> documents = loader.load()
            >>> print(len(documents))
            1
        """
        logger.debug(f"DocxLoader loading file: {self.file_path}")
        
        full_path = self._get_full_path()
        logger.debug(f"Full path: {full_path}")
        
        if not os.path.exists(full_path):
            logger.error(f"File does not exist at: {full_path}")
            raise FileNotFoundError(f"File not found: {full_path}")
        
        logger.info(f"File found at: {full_path}")
        
        try:
            loader = Docx2txtLoader(full_path)
            documents = loader.load()
            logger.info(f"Successfully loaded DOCX file with {len(documents)} document(s).")
            return documents
        except Exception as e:
            logger.error(f"Error loading DOCX file: {str(e)}")
            raise

    def load_and_split(self) -> List[Document]:
        """
        Load the DOCX file, split it into chunks, and return a list of Document objects.

        This method reads the DOCX file from the specified path, converts it
        into a list of Document objects, splits the documents into smaller chunks,
        and returns the list of chunks.

        Returns:
            List[Document]: A list of Document objects split into chunks.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
            Exception: For any other errors during loading or splitting.

        Example:
            >>> loader = DocxLoader("/path/to/your/docx/file.docx")
            >>> split_documents = loader.load_and_split()
            >>> print(len(split_documents))
            10
        """
        documents = self.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(documents)
        logger.info(f"Split DOCX document into {len(split_docs)} chunks.")
        return split_docs
