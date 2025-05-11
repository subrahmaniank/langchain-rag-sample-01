import logging


def setup_logger(name: str) -> logging.Logger:
    """
    Set up and configure a logger with the given name.

    This function creates a logger with the specified name, sets its level to DEBUG,
    and adds a StreamHandler that outputs to the console. The log messages are
    formatted to include the timestamp, logger name, log level, and message.

    Args:
        name (str): The name of the logger. This is typically the __name__ of the
                    module where the logger is being created.

    Returns:
        logging.Logger: A configured logger object ready for use.

    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.debug("This is a debug message")
        2023-07-09 18:30:15,123 - my_module - DEBUG - This is a debug message
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger
