"""
Lexical retriever using OpenSearch (BM25).
"""

import logging

from app.retrieval.hybrid.models import HybridSearchResult
from app.retrieval.lexical.opensearch_service import OpenSearchService

logger = logging.getLogger(__name__)


class LexicalRetriever:
    """
    Performs lexical search using OpenSearch.
    """

    def __init__(self) -> None:

        self._opensearch = OpenSearchService()

    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[HybridSearchResult]:
        """
        Perform lexical search.

        Args:
            query:
                User query.

            top_k:
                Number of search results.

        Returns:
            List of hybrid search results.
        """

        try:
            hits = self._opensearch.search(
                query=query,
                top_k=top_k,
            )

        except Exception as ex:

            logger.warning(
                "OpenSearch search failed. Falling back to semantic search only. Error: %s",
                ex,
            )

            return []

        results = []

        for hit in hits:

            source = hit["_source"]

            results.append(
                HybridSearchResult(
                    chunk_id=source["chunk_id"],
                    document_id=source["document_id"],
                    source_path=source["source_path"],
                    extension=source["extension"],
                    content=source["content"],
                    score=hit["_score"],
                )
            )

        return results