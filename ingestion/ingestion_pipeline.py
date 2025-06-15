import os
import time

from dotenv import load_dotenv
from watchdog.observers import Observer

from ingestion.ingestion_pipeline_handler import IngestionPipelineHandler
from ingestion.universal_embedder import UniversalEmbedder
from ingestion.universal_loader import UniversalLoader
from ingestion.universal_splitter import UniversalSplitter
from logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv(override=False)


class IngestionPipeline:

    def __init__(self):
        file_path = os.getenv("INGESTION_SOURCE_PATH", ".")

        logger.debug(f"ingestion_pipeline function received file_path: {file_path}")

        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"Error: Incorrect path configured : {file_path}")
            raise ValueError(f"Error: Incorrect path configured: {file_path}")

        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Directory contents: {os.listdir(os.path.dirname(file_path))}")

        self.file_path = file_path

    def run(self):
        self.watch_directory(self.file_path, self.process_document)

    def watch_directory(self, path, process_function):
        event_handler = IngestionPipelineHandler(process_function)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def process_document(self, file_path):
        loader = UniversalLoader(file_path)
        splitter = UniversalSplitter()
        embedder = UniversalEmbedder()
        try:
            documents = loader.load()
            logger.info(f"Successfully loaded {len(documents)} documents.")
            # Process documents further as needed
            chunks = splitter.split_documents(documents)
            logger.info(f"Successfully split {len(chunks)} chunks.")

            # loop through the chunks and print them
            if logger.debug:
                for chunk in chunks:
                    print(chunk.page_content)
                    print("-" * 80)

            embeddings = embedder.embed_documents(chunks)
            logger.info(f"Successfully embedded {len(embeddings)} embeddings.")

        except FileNotFoundError as e:
            logger.error(
                f"Error: The file was not found. Please check the file path: {e}"
            )
        except PermissionError as e:
            logger.error(
                f"Error: Permission denied when trying to access the file: {e}"
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
