"""
Document reranking service.
"""

from app.ai.reranker.cross_encoder_service import CrossEncoderService
from app.rag.models import SearchResult


class Reranker:
    """
    Reranks retrieved search results using a CrossEncoder model.
    """

    def __init__(self) -> None:
        self._cross_encoder = CrossEncoderService()

    async def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Rerank retrieved search results.

        Args:
            query:
                User query.

            results:
                Retrieved search results.

            top_k:
                Number of documents to return after reranking.

        Returns:
            Reranked search results.
        """

        if not results:
            return []

        #
        # Extract document text
        #

        documents = [
            result.chunk.content
            for result in results
        ]

        #
        # Compute relevance scores
        #

        scores = self._cross_encoder.rerank(
            query=query,
            documents=documents,
        )

        #
        # Pair results with scores
        #

        reranked = list(zip(results, scores))

        #
        # Sort by descending score
        #

        reranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        #
        # Update SearchResult scores
        #

        final_results = []

        for result, score in reranked:
            result.score = score
            final_results.append(result)

        return final_results[:top_k]