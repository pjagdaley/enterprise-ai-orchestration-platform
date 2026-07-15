"""
Shared models for the RAG module.
"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from typing import Any


class DocumentChunk(BaseModel):
    """
    Represents a chunk of a document.
    """

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(
        ...,
        description="Unique document identifier."
    )

    chunk_id: str = Field(
        ...,
        description="Unique chunk identifier."
    )

    content: str = Field(
        ...,
        description="Chunk text."
    )

    source: str = Field(
        ...,
        description="Original document path."
    )

    page_number: int | None = Field(
        default=None,
        description="Page number, if applicable."
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional document metadata."
    )


class SearchRequest(BaseModel):
    """
    Semantic search request.
    """

    model_config = ConfigDict(extra="forbid")

    query: str = Field(
        ...,
        description="Search query."
    )

    top_k: int = Field(
        default=5,
        gt=0,
        le=20,
        description="Maximum number of results."
    )


class SearchResult(BaseModel):
    """
    Retrieved document chunk.
    """

    model_config = ConfigDict(extra="forbid")

    chunk: DocumentChunk

    score: float = Field(
        ...,
        description="Similarity score."
    )