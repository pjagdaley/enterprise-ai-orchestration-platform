"""
Router configuration.
"""

from fastapi import FastAPI

from app.api.router import router as api_router


def configure_routers(app: FastAPI) -> None:
    """
    Register API routers.
    """

    app.include_router(api_router)