from watchdog.events import FileSystemEventHandler

from logging_config import setup_logger


logger = setup_logger(__name__)


class IngestionPipelineHandler(FileSystemEventHandler):
    def __init__(self, process_function):
        self.process_function = process_function

    def on_created(self, event):
        if not event.is_directory:
            logger.debug(f"New document detected: {event.src_path}")
            self.process_function(event.src_path)
