"""
Middleware configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.middleware.access_logging import AccessLoggingMiddleware


def configure_middleware(app: FastAPI) -> None:
    """
    Configure application middleware.
    """

    #
    # CORS
    #
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    #
    # GZip Compression
    #
    if settings.gzip_enabled:
        app.add_middleware(
            GZipMiddleware,
            minimum_size=settings.gzip_minimum_size,
        )

    #
    # Access Logging
    #
    app.add_middleware(
        AccessLoggingMiddleware,
    )