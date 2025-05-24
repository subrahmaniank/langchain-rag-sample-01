import os
from typing import List, override
from urllib.parse import unquote

from dotenv import load_dotenv
from langchain.schema import Document
import pymupdf

from ingestion.loaders.abstract_document_loader import AbstractDocumentLoader
from logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv()


class PDFLoader(AbstractDocumentLoader):
    """
    A class for loading and processing PDF documents using PyMuPDF (fitz).

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
        Load the PDF file and return a list of Document objects using PyMuPDF (fitz).

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
            source_docs = pymupdf.open(full_path)
            logger.info(f"PDF loaded successfully. Number of pages: {len(source_docs)}")
            documents = []
            # iterate the document pages and create a document object for each page
            i = 0
            for page in source_docs:
                i = i + 1
                document = Document(
                    page_content=page.get_text(),  # type: ignore
                    metadata={
                        "page": i,
                        "location": full_path,
                        "file_name": os.path.basename(full_path),
                        "file_extension": os.path.splitext(full_path)[1],
                    },
                )
                documents.append(document)
            return documents

        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            raise

    @override
    def load_and_split(self) -> List[Document]:
        return super().load_and_split()
