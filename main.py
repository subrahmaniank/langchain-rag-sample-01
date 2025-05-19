import os
import sys
from ingestion.universal_loader import UniversalLoader
from ingestion.universal_splitter import UniversalSplitter
from logging_config import setup_logger

logger = setup_logger(__name__)


def ingestion_pipeline(file_path):
    logger.debug(f"ingestion_pipeline function received file_path: {file_path}")

    # Check if the file exists
    if not os.path.exists(file_path):
        logger.error(
            f"Error: The file does not exist at the specified path: {file_path}"
        )
        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Directory contents: {os.listdir(os.path.dirname(file_path))}")
        return

    loader = UniversalLoader(file_path)
    try:
        documents = loader.load()
        logger.info(f"Successfully loaded {len(documents)} documents.")
        # Process documents further as needed
        splitter = UniversalSplitter()
        chunks = splitter.split_documents(documents)
        logger.info(f"Successfully split {len(chunks)} chunks.")
    except FileNotFoundError as e:
        logger.error(f"Error: The file was not found. Please check the file path: {e}")
    except PermissionError as e:
        logger.error(f"Error: Permission denied when trying to access the file: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def main(file_path):
    ingestion_pipeline(file_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    main(file_path)
