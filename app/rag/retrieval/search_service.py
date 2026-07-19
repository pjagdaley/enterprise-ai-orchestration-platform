"""
Hybrid search service.
"""

from app.rag.models import DocumentChunk
from app.rag.models import SearchRequest
from app.rag.models import SearchResult
from app.retrieval.hybrid.hybrid_retriever import HybridRetriever


class SearchService:
    """
    Service responsible for hybrid retrieval.
    """

    def __init__(self) -> None:

        self._hybrid = HybridRetriever()

    async def search(
        self,
        request: SearchRequest,
    ) -> list[SearchResult]:
        """
        Perform hybrid retrieval.
        """

        hits = await self._hybrid.search(
            query=request.query,
            top_k=request.top_k,
        )

        results: list[SearchResult] = []

        for hit in hits:

            chunk = DocumentChunk(
                document_id=hit.document_id,
                chunk_id=hit.chunk_id,
                content=hit.content,
                source=hit.source_path,
                page_number=None,
                metadata={},
            )

            results.append(
                SearchResult(
                    chunk=chunk,
                    score=hit.score,
                )
            )

        return results