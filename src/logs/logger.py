import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_FORMAT, LOGS_DIR


def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger with both file and console handlers.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_file = LOGS_DIR / f"{name}.log"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Create default logger
logger = setup_logger("hate_speech_detection")
