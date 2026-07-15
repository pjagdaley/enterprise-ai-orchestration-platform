"""
Document reranking service.
"""

from app.rag.models import SearchResult


class Reranker:
    """
    Reranks retrieved search results.

    The current implementation returns the results unchanged.
    A real reranker (e.g. BGE, Cohere, Vertex AI Ranking)
    can be integrated later without affecting callers.
    """

    async def rerank(
        self,
        query: str,
        results: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Rerank retrieved documents.

        Args:
            query:
                User query.

            results:
                Retrieved search results.

        Returns:
            Reranked search results.
        """

        # Placeholder implementation.
        # Future versions will rerank using a cross-encoder model.

        return results