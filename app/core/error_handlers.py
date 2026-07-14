"""
Global exception handlers.
"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationException
from app.schemas.error import ErrorResponse

logger = logging.getLogger(__name__)


async def application_exception_handler(
    request: Request,
    exc: ApplicationException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=exc.error_code,
            message=exc.message,
        ).model_dump(),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception("Unhandled exception")

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred.",
        ).model_dump(),
    )