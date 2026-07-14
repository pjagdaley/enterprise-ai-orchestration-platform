"""
Logging configuration for the Enterprise AI Orchestration Platform.
"""

import logging
import logging.handlers
from pathlib import Path

from app.core.config import settings
from app.core.logging.formatters import EnterpriseFormatter
from app.core.logging.config import LOG_FORMAT, DATE_FORMAT

def configure_logging() -> None:
    """
    Configure application logging.
    """

    log_directory = Path(settings.log_dir)
    log_directory.mkdir(exist_ok=True)

    formatter = EnterpriseFormatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level.upper())

    root_logger.handlers.clear()

    #
    # Console Handler
    #
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    #
    # Rotating File Handler
    #
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_directory / settings.log_file,
        maxBytes=10 * 1024 * 1024,   # 10 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance.

    Example:
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)