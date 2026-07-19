"""
Document ingestion service.
"""

import uuid
from pathlib import Path

from app.infrastructure.qdrant.qdrant_service import QdrantService
from app.infrastructure.vertexai.embedding_service import EmbeddingService
from app.rag.ingestion.chunker import DocumentChunker
from app.rag.ingestion.parsers import DocumentParser

from app.retrieval.lexical.opensearch_service import OpenSearchService


class IngestService:
    """
    Service responsible for ingesting documents into the
    Enterprise Knowledge Base.
    """

    def __init__(self) -> None:

        self._parser = DocumentParser()

        self._chunker = DocumentChunker()

        self._embedding_service = EmbeddingService()

        self._qdrant = QdrantService()

        self._opensearch = OpenSearchService()

    async def ingest(
        self,
        file_path: str,
    ) -> int:
        """
        Ingest a document.

        Returns:
            Number of chunks indexed.
        """

        #
        # Generate Document ID
        #

        document_id = str(uuid.uuid4())

        #
        # Parse
        #

        text = self._parser.parse(file_path)

        #
        # Chunk
        #

        chunks = self._chunker.chunk_document(
            document_id=document_id,
            source=file_path,
            text=text,
        )

        #
        # Embed + Store
        #

        for chunk in chunks:

            embedding = await self._embedding_service.embed_document(
                chunk.content
            )

            await self._qdrant.upsert(
                chunk=chunk,
                embedding=embedding,
            )

            self._opensearch.index_document(
                {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "source_path": chunk.source,
                    "extension": Path(chunk.source).suffix.lower(),
                    "content": chunk.content,
                }
            )

        return len(chunks)