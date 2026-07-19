"""
Reciprocal Rank Fusion (RRF).
"""

from collections import defaultdict

from app.retrieval.hybrid.models import HybridSearchResult


class MergeService:
    """
    Merge retrieval results using Reciprocal Rank Fusion.
    """

    RRF_K = 60

    def merge(
        self,
        semantic_results: list[HybridSearchResult],
        lexical_results: list[HybridSearchResult],
        top_k: int = 5,
    ) -> list[HybridSearchResult]:

        scores: dict[str, float] = defaultdict(float)

        documents: dict[str, HybridSearchResult] = {}

        #
        # Semantic ranking
        #

        for rank, result in enumerate(
            semantic_results,
            start=1,
        ):

            scores[result.chunk_id] += 1 / (
                self.RRF_K + rank
            )

            documents[result.chunk_id] = result

        #
        # Lexical ranking
        #

        for rank, result in enumerate(
            lexical_results,
            start=1,
        ):

            scores[result.chunk_id] += 1 / (
                self.RRF_K + rank
            )

            documents[result.chunk_id] = result

        #
        # Sort
        #

        merged = sorted(
            documents.values(),
            key=lambda doc: scores[doc.chunk_id],
            reverse=True,
        )

        #
        # Update scores
        #

        for document in merged:

            document.score = scores[
                document.chunk_id
            ]

        return merged[:top_k]