"""
Vertex AI embedding service.
"""

from google.genai.types import EmbedContentConfig

from app.core.config import settings
from app.infrastructure.vertexai.client import VertexAIClient


class EmbeddingService:
    """
    Service for generating text embeddings using Vertex AI.
    """

    def __init__(
        self,
        client: VertexAIClient | None = None,
    ) -> None:
        """
        Initialize the embedding service.
        """

        self._vertex_client = client or VertexAIClient()
        self._client = self._vertex_client.client
        self._model = settings.embedding_model

    async def embed_document(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a document chunk.
        """

        return await self._embed(
            text=text,
            task_type="RETRIEVAL_DOCUMENT",
        )

    async def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a search query.
        """

        return await self._embed(
            text=text,
            task_type="RETRIEVAL_QUERY",
        )

    async def _embed(
        self,
        text: str,
        task_type: str,
    ) -> list[float]:
        """
        Generate an embedding.

        Args:
            text:
                Input text.

            task_type:
                Vertex AI embedding task type.

        Returns:
            Embedding vector.
        """

        response = self._client.models.embed_content(
            model=self._model,
            contents=text,
            config=EmbedContentConfig(
                task_type=task_type,
            ),
        )

        return response.embeddings[0].values