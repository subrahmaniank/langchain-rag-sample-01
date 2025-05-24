from ingestion.ingestion_pipeline import IngestionPipeline
from logging_config import setup_logger

logger = setup_logger(__name__)


def main():
    """
    Main function to run the ingestion pipeline.
    """
    logger.info("Starting ingestion pipeline...")
    ingestion_pipeline = IngestionPipeline()
    ingestion_pipeline.run()
    logger.info("Ingestion pipeline completed.")


if __name__ == "__main__":
    main()
