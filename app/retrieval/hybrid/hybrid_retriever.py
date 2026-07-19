"""
Hybrid retriever using Reciprocal Rank Fusion (RRF).
"""

from app.retrieval.hybrid.merge_service import MergeService
from app.retrieval.hybrid.models import HybridSearchResult
from app.retrieval.lexical.lexical_retriever import LexicalRetriever
from app.retrieval.semantic.semantic_retriever import SemanticRetriever

class HybridRetriever:
    """
    Performs hybrid retrieval using semantic and lexical search.
    """

    def __init__(self) -> None:

        self._semantic = SemanticRetriever()

        self._lexical = LexicalRetriever()

        self._merge_service = MergeService()

    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[HybridSearchResult]:
        """
        Perform hybrid retrieval.

        Args:
            query:
                User query.

            top_k:
                Number of final results.

        Returns:
            Ranked hybrid search results.
        """

        #
        # Semantic Search
        #

        semantic_results = await self._semantic.search(
            query=query,
            top_k=top_k,
        )

        #
        # Lexical Search
        #

        lexical_results = await self._lexical.search(
            query=query,
            top_k=top_k,
        )        

        #
        # Merge using RRF
        #

        return self._merge_service.merge(
            semantic_results,
            lexical_results,
            top_k=top_k,
        )