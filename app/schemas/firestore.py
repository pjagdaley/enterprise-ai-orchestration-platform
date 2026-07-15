"""
Firestore document metadata schema.
"""

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.domain.enums.document_status import DocumentStatus
from app.domain.enums.source_type import DocumentSourceType


class DocumentMetadata(BaseModel):
    """
    Metadata stored for each indexed document.
    """

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(
        ...,
        description="Unique document identifier."
    )

    source_path: str = Field(
        ...,
        description="Full path of the source document."
    )

    source_type: DocumentSourceType = Field(
        default=DocumentSourceType.LOCAL,
        description="Source of the document."
    )

    generation: str = Field(
        ...,
        description="Generation/version of the source document."
    )

    extension: str = Field(
        ...,
        description="File extension."
    )

    content_type: str = Field(
        ...,
        description="Document MIME content type."
    )

    status: DocumentStatus = Field(
        default=DocumentStatus.PENDING,
        description="Current document status."
    )

    chunk_count: int = Field(
        default=0,
        ge=0,
        description="Number of indexed chunks."
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Document creation timestamp."
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp."
    )

    last_error: str | None = Field(
        default=None,
        description="Last ingestion error."
    )