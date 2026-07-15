"""
Qdrant vector database service.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams

from app.core.config import settings
from app.rag.models import DocumentChunk


class QdrantService:
    """
    Service for interacting with Qdrant.
    """

    def __init__(self) -> None:

        self._client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )

        self._collection = settings.qdrant_collection

        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """
        Create the collection if it does not exist.
        """

        collections = self._client.get_collections().collections

        names = [
            collection.name
            for collection in collections
        ]

        if self._collection not in names:

            self._client.create_collection(
                collection_name=self._collection,
                vectors_config=VectorParams(
                    size=768,
                    distance=Distance.COSINE,
                ),
            )

    async def upsert(
        self,
        chunk: DocumentChunk,
        embedding: list[float],
    ) -> None:
        """
        Store a document chunk.
        """

        self._client.upsert(
            collection_name=self._collection,
            points=[
                PointStruct(
                    id=chunk.chunk_id,
                    vector=embedding,
                    payload={
                        "document_id": chunk.document_id,
                        "source": chunk.source,
                        "content": chunk.content,
                        "page_number": chunk.page_number,
                        "metadata": chunk.metadata,
                    },
                )
            ],
        )

    async def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ):
        """
        Search similar document chunks.
        """

        response = self._client.query_points(
            collection_name=self._collection,
            query=embedding,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        return response.points