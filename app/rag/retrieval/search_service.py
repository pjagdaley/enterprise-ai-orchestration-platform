"""
Semantic search service.
"""

from app.infrastructure.qdrant.qdrant_service import QdrantService
from app.infrastructure.vertexai.embedding_service import EmbeddingService
from app.rag.models import DocumentChunk
from app.rag.models import SearchRequest
from app.rag.models import SearchResult


class SearchService:
    """
    Service responsible for semantic search.
    """

    def __init__(self) -> None:

        self._embedding_service = EmbeddingService()

        self._qdrant = QdrantService()

    async def search(
        self,
        request: SearchRequest,
    ) -> list[SearchResult]:
        """
        Perform semantic search.

        Args:
            request:
                Search request.

        Returns:
            Search results.
        """

        #
        # Embed query
        #

        embedding = await self._embedding_service.embed_query(
            request.query
        )

        #
        # Search Qdrant
        #

        hits = await self._qdrant.search(
            embedding=embedding,
            top_k=request.top_k,
        )

        results: list[SearchResult] = []

        for hit in hits:

            payload = hit.payload

            chunk = DocumentChunk(
                document_id=payload["document_id"],
                chunk_id=str(hit.id),
                content=payload["content"],
                source=payload["source"],
                page_number=payload.get("page_number"),
                metadata=payload.get("metadata", {}),
            )

            results.append(
                SearchResult(
                    chunk=chunk,
                    score=hit.score,
                )
            )

        return results