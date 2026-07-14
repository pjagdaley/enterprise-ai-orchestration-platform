"""
Application logging bootstrap.

Initializes the logging subsystem during application startup.
"""

from app.core.logging.logger import configure_logging


def configure_application_logging() -> None:
    """
    Configure the application logging subsystem.
    """

    configure_logging()