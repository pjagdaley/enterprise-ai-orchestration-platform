"""
Semantic retriever using Qdrant.
"""

from app.infrastructure.qdrant.qdrant_service import QdrantService
from app.infrastructure.vertexai.embedding_service import EmbeddingService
from app.retrieval.hybrid.models import HybridSearchResult


class SemanticRetriever:
    """
    Performs semantic retrieval using vector search.
    """

    def __init__(self) -> None:

        self._embedding_service = EmbeddingService()

        self._qdrant = QdrantService()

    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[HybridSearchResult]:
        """
        Perform semantic search.

        Args:
            query:
                User query.

            top_k:
                Number of results.

        Returns:
            Semantic search results.
        """

        #
        # Generate embedding
        #

        embedding = await self._embedding_service.embed_query(
            query
        )

        #
        # Vector search
        #

        results = await self._qdrant.search(
            embedding=embedding,
            top_k=top_k,
        )

        #
        # Convert to common model
        #

        search_results = []

        for result in results:

            payload = result.payload
            
            search_results.append(
                HybridSearchResult(
                    chunk_id=payload["chunk_id"],
                    document_id=payload["document_id"],
                    source_path=payload["source_path"],
                    extension=payload["extension"],
                    content=payload["content"],
                    score=result.score,
                )
            )

        return search_results