import os

from ingestion.loaders import AbstractDocumentLoader, DocxLoader, PDFLoader, TextLoader
from logging_config import setup_logger

logger = setup_logger(__name__)


class UniversalLoader:
    def __init__(self, file_path):
        """
        Initialize a new instance of the class.

        This constructor sets up the instance with the provided file path.

        Args:
            file_path (str): The path to the file that will be loaded and processed.

        Attributes:
            file_path (str): Stores the path to the file for later use in loading and processing.

        """
        self.file_path = file_path

    def get_loader(self) -> AbstractDocumentLoader:
        """
        Determine and return the appropriate document loader based on the file extension.

        This method examines the extension of the file specified by self.file_path
        and returns the corresponding loader class instance.

        Returns:
            AbstractDocumentLoader: An instance of the appropriate document loader.

        Supported file types and their loaders:
        - .pdf: PDFLoader
        - .txt, .md, .log: TextLoader
        - .docx: DocxLoader

        Raises:
            ValueError: If the file extension is not supported.

        """
        file_extension = os.path.splitext(self.file_path)[1].lower()

        if file_extension == ".pdf":
            return PDFLoader(self.file_path)
        elif file_extension in [".txt", ".md", ".log"]:
            return TextLoader(self.file_path)
        elif file_extension == ".docx":
            return DocxLoader(self.file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def load(self):
        """
        Load documents from the specified file path.

        This method attempts to load the file specified by self.file_path using
        the appropriate loader determined by the get_loader method.

        Returns:
            list: A list of loaded documents.

        Raises:
            FileNotFoundError: If the specified file is not found.
            PermissionError: If there's no permission to access the file.
            Exception: For any other unexpected errors during the loading process.

        Logs:
            - Info: Attempt to load file and successful loading of documents.
            - Error: Any errors encountered during the loading process.

        """
        logger.info(f"Attempting to load file: {self.file_path}")

        try:
            loader = self.get_loader()
            documents = loader.load()
            logger.info(f"Successfully loaded {len(documents)} documents.")
            return documents
        except FileNotFoundError as e:
            logger.error(f"Error: File not found - {e}")
            raise
        except PermissionError as e:
            logger.error(f"Error: Permission denied - {e}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while loading the document: {str(e)}"
            )
            raise

    def load_and_split(self):
        """
        Load and split documents from the specified file path.

        This method attempts to load the file specified by self.file_path using
        the appropriate loader determined by the get_loader method, and then
        splits the loaded content into smaller chunks.

        Returns:
            list: A list of split document chunks.

        Raises:
            FileNotFoundError: If the specified file is not found.
            PermissionError: If there's no permission to access the file.
            Exception: For any other unexpected errors during the loading and splitting process.

        Logs:
            - Info: Attempt to load and split file, and successful loading and splitting of documents.
            - Error: Any errors encountered during the loading and splitting process.

        """
        logger.info(f"Attempting to load and split file: {self.file_path}")

        try:
            loader = self.get_loader()
            split_documents = loader.load_and_split()
            logger.info(
                f"Successfully loaded and split into {len(split_documents)} chunks."
            )
            return split_documents
        except FileNotFoundError as e:
            logger.error(f"Error: File not found - {e}")
            raise
        except PermissionError as e:
            logger.error(f"Error: Permission denied - {e}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while loading and splitting the document: {str(e)}"
            )
            raise
