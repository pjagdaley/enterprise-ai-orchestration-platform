"""
Exception handler configuration.
"""

from fastapi import FastAPI

from app.core.error_handlers import (
    application_exception_handler,
    unhandled_exception_handler,
)
from app.core.exceptions import ApplicationException


def configure_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """

    app.add_exception_handler(
        ApplicationException,
        application_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )