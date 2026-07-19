"""
Cross Encoder service.

Provides a reusable interface for document reranking.
"""

from sentence_transformers import CrossEncoder
from app.core.config import settings

class CrossEncoderService:
    """
    Cross Encoder inference service.
    """

    def __init__(self) -> None:
        """
        Load the reranker model.
        """

        #
        # Fast production model
        #

        self._model = CrossEncoder(
            settings.reranker_model
        )

        #
        # Alternative models
        #

        # self._model = CrossEncoder(
        #     "BAAI/bge-reranker-v2-m3"
        # )

        # self._model = CrossEncoder(
        #     "BAAI/bge-reranker-base"
        # )

    def rerank(
        self,
        query: str,
        documents: list[str],
    ) -> list[float]:
        """
        Compute relevance scores.

        Args:
            query:
                User query.

            documents:
                Retrieved document texts.

        Returns:
            Relevance scores.
        """

        if not documents:
            return []

        pairs = [
            (query, document)
            for document in documents
        ]

        scores = self._model.predict(
            pairs
        )

        return [
            float(score)
            for score in scores
        ]