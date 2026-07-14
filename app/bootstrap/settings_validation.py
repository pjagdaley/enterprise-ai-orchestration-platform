"""
Application settings validation.

Validates critical application configuration during startup.
"""

from app.core.config import settings
from app.core.logging.logger import get_logger

logger = get_logger(__name__)


class SettingsValidationError(RuntimeError):
    """Raised when application settings are invalid."""


def validate_settings() -> None:
    """
    Validate all required application settings.

    Raises:
        SettingsValidationError:
            If any required configuration is invalid.
    """

    logger.info("Validating application configuration...")

    #
    # Google Cloud
    #
    _validate_required(settings.project_id, "PROJECT_ID")
    _validate_required(settings.location, "LOCATION")
    _validate_required(settings.gcs_bucket, "GCS_BUCKET")

    #
    # Vertex AI
    #
    _validate_required(settings.gemini_model, "GEMINI_MODEL")
    _validate_required(settings.embedding_model, "EMBEDDING_MODEL")

    #
    # Qdrant
    #
    _validate_required(settings.qdrant_host, "QDRANT_HOST")
    _validate_required(settings.qdrant_collection, "QDRANT_COLLECTION")

    if settings.qdrant_port <= 0:
        raise SettingsValidationError(
            "QDRANT_PORT must be greater than zero."
        )

    #
    # Retrieval
    #
    if settings.chunk_size <= 0:
        raise SettingsValidationError(
            "CHUNK_SIZE must be greater than zero."
        )

    if settings.chunk_overlap < 0:
        raise SettingsValidationError(
            "CHUNK_OVERLAP cannot be negative."
        )

    if settings.top_k <= 0:
        raise SettingsValidationError(
            "TOP_K must be greater than zero."
        )

    if settings.rerank_top_k <= 0:
        raise SettingsValidationError(
            "RERANK_TOP_K must be greater than zero."
        )

    if settings.rerank_top_k > settings.top_k:
        raise SettingsValidationError(
            "RERANK_TOP_K cannot be greater than TOP_K."
        )

    logger.info("Application configuration validation completed successfully.")


def _validate_required(value: str | None, setting_name: str) -> None:
    """
    Validate that a required setting has a value.
    """

    if value is None or str(value).strip() == "":
        raise SettingsValidationError(
            f"Required setting '{setting_name}' is missing."
        )