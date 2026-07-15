"""
Application configuration.

Loads configuration from:
1. Environment variables
2. .env file (for local development)

Cloud Run will automatically override .env values using environment variables.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # Application
    # ==========================================================
    app_name: str = Field(
        default="Enterprise AI Orchestration Platform",
        description="Application name",
    )

    app_version: str = Field(
        default="1.0.0",
        description="Application version",
    )

    environment: str = Field(
        default="local",
        description="local | dev | test | stage | prod",
    )

    debug: bool = Field(default=True)

    api_prefix: str = Field(default="/api/v1")

    # ==========================================================
    # Google Cloud
    # ==========================================================
    project_id: str

    location: str = "us-central1"

    gcs_bucket: str

    # ==========================================================
    # Vertex AI
    # ==========================================================
    gemini_model: str = "gemini-2.5-flash"

    embedding_model: str = "text-embedding-005"

    # ==========================================================
    # Firestore
    # ==========================================================
    firestore_database: str = "(default)"

    # ==========================================================
    # Qdrant
    # ==========================================================
    qdrant_host: str = "localhost"

    qdrant_port: int = 6333

    qdrant_collection: str

    # ==========================================================
    # Retrieval
    # ==========================================================
    chunk_size: int = 1500

    chunk_overlap: int = 300

    embedding_batch_size: int = 40

    top_k: int = 10

    rerank_top_k: int = 5

    # ==========================================================
    # Logging
    # ==========================================================
    log_level: str = "INFO"

    log_dir: str = "logs"

    log_file: str = "application.log"
    
    # ==========================================================
    # API
    # ==========================================================
    request_timeout: int = 120

    # ==========================================================
    # CORS
    # ==========================================================

    cors_origins: list[str] = [
        "http://localhost:3000",
    ]

    cors_allow_credentials: bool = True

    cors_allow_methods: list[str] = ["*"]

    cors_allow_headers: list[str] = ["*"]

    # ==========================================================
    # GZip Compression
    # ==========================================================

    gzip_enabled: bool = True

    gzip_minimum_size: int = 1000

    # ==========================================================
    # Security (Future)
    # ==========================================================
    jwt_secret: str | None = None

    jwt_algorithm: str = "HS256"

    jwt_expiry_minutes: int = 60

   # ==========================================================
    # LLM
    # ==========================================================

    llm_provider: str = "mock"

    gemini_model: str = "gemini-2.5-flash"

    vertex_ai_location: str = "us-central1"

    project_id: str

    # ==========================================================
    # Chunking
    # ==========================================================

    chunk_size: int = 1500

    chunk_overlap: int = 300

    # ==========================================================
    # Embeddings
    # ==========================================================

    embedding_model: str = "text-embedding-005"

    # ==========================================================
    # Qdrant
    # ==========================================================

    qdrant_host: str = "localhost"

    qdrant_port: int = 6333

    qdrant_collection: str = "enterprise_documents"

    # ==========================================================
    # Firestore
    # ==========================================================

    firebase_credentials_path: str


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Using lru_cache ensures the configuration is loaded only once.
    """
    return Settings()


settings = get_settings()