"""
Common dependency providers.

This module contains reusable FastAPI dependency providers that can be
shared across API endpoints.
"""

from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings


def get_app_settings() -> Settings:
    """
    Returns the application settings singleton.
    """
    return get_settings()


# Type alias for cleaner dependency injection
SettingsDep = Annotated[Settings, Depends(get_app_settings)]