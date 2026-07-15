"""
Document chunking service.
"""

import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.rag.models import DocumentChunk


class DocumentChunker:
    """
    Splits documents into chunks suitable for embedding.
    """

    def __init__(self) -> None:
        """
        Initialize the text splitter.
        """

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def chunk_document(
        self,
        document_id: str,
        source: str,
        text: str,
    ) -> list[DocumentChunk]:
        """
        Split a document into chunks.

        Args:
            document_id:
                Unique document identifier.

            source:
                Source document path.

            text:
                Extracted document text.

        Returns:
            List of document chunks.
        """

        chunks = self._splitter.split_text(text)

        results: list[DocumentChunk] = []

        for chunk in chunks:

            results.append(
                DocumentChunk(
                    document_id=document_id,
                    chunk_id=str(uuid.uuid4()),
                    content=chunk,
                    source=source,
                )
            )

        return results