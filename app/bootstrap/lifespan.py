"""
Application lifespan management.

Responsible for startup and shutdown of shared application resources.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging.logger import get_logger

from app.bootstrap.settings_validation import validate_settings

from app.bootstrap.services import ApplicationServices

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    #
    # Startup
    #
    logger.info("=" * 80)
    logger.info("Starting Enterprise AI Orchestration Platform")
    logger.info("Environment : %s", settings.environment)
    logger.info("Version     : %s", settings.app_version)
    logger.info("=" * 80)

    #
    # Future Startup Tasks
    #
    validate_settings()
    # initialize_firestore()
    # initialize_vertex_ai()
    # initialize_qdrant()
    # initialize_mcp()
    # initialize_tool_registry()

    services = ApplicationServices()
    await services.initialize()

    app.state.services = services

    yield

    #
    # Shutdown
    #
    logger.info("=" * 80)
    logger.info("Shutting down Enterprise AI Orchestration Platform")
    logger.info("=" * 80)

    #
    # Future Cleanup
    #
    # close_firestore()
    # close_qdrant()
    # close_scheduler()
    await services.shutdown()