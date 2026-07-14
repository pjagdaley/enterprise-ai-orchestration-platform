"""
Application factory for the Enterprise AI Orchestration Platform.

Responsible for creating and configuring the FastAPI application.
"""

from fastapi import FastAPI

from app.bootstrap.exception_handlers import configure_exception_handlers
from app.bootstrap.logging import configure_application_logging
from app.bootstrap.middleware import configure_middleware
from app.bootstrap.routers import configure_routers
from app.core.config import settings

from app.bootstrap.lifespan import lifespan
from app.bootstrap.openapi import configure_openapi


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    #
    # Configure logging
    #
    configure_application_logging()

    #
    # Create FastAPI application
    #
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    configure_openapi(app)

    #
    # Configure middleware
    #
    configure_middleware(app)

    #
    # Configure exception handlers
    #
    configure_exception_handlers(app)

    #
    # Configure routers
    #
    configure_routers(app)
    
    return app