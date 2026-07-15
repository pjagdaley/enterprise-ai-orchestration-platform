"""
Document schemas.
"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class DocumentUploadResponse(BaseModel):
    """
    Response returned after a document is uploaded
    and indexed successfully.
    """

    model_config = ConfigDict(extra="forbid")

    filename: str = Field(
        ...,
        description="Uploaded file name."
    )

    chunks_indexed: int = Field(
        ...,
        ge=0,
        description="Number of chunks indexed."
    )

    message: str = Field(
        ...,
        description="Status message."
    )


class DocumentInfo(BaseModel):
    """
    Basic information about an indexed document.
    """

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(
        ...,
        description="Unique document identifier."
    )

    filename: str = Field(
        ...,
        description="Document name."
    )

    chunk_count: int = Field(
        ...,
        ge=0,
        description="Number of indexed chunks."
    )