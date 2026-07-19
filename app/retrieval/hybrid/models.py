"""
Hybrid retrieval models.
"""

from pydantic import BaseModel


class HybridSearchResult(BaseModel):
    """
    Unified retrieval result.
    """

    chunk_id: str

    document_id: str

    source_path: str

    extension: str

    content: str

    score: float