"""
Document application service.
"""

import uuid
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile
from starlette import status

from app.domain.enums.source_type import DocumentSourceType
from app.domain.enums.document_status import DocumentStatus
from app.infrastructure.firestore.firestore_service import FirestoreService
from app.infrastructure.storage.gcs_storage import GCSStorage
from app.rag.ingestion.ingest_service import IngestService
from app.schemas.document import DocumentUploadResponse
from app.schemas.firestore import DocumentMetadata


class DocumentService:
    """
    Service responsible for document upload and ingestion.
    """

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
        ".json",
        ".xlsx",
    }

    def __init__(self) -> None:

        self._storage = GCSStorage()

        self._ingest_service = IngestService()

        self._firestore_service = FirestoreService()

    async def upload_document(
        self,
        file: UploadFile,
    ) -> DocumentUploadResponse:
        """
        Upload and ingest a document.
        """

        #
        # Validate extension
        #

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {extension}",
            )

        #
        # Upload to Google Cloud Storage
        #

        storage_path = await self._storage.upload(
            file
        )

        #
        # Create metadata
        #

        metadata = DocumentMetadata(
            document_id=str(uuid.uuid4()),
            source_path=storage_path,
            generation="1",
            extension=extension,
            content_type=file.content_type
            or "application/octet-stream",
            source_type=DocumentSourceType.GCS,
            status=DocumentStatus.PROCESSING,
            chunk_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_error=None,
        )

        await self._firestore_service.save_document(
            metadata
        )

        try:

            #
            # Ingest from GCS
            #

            chunk_count = await self._ingest_service.ingest(
                storage_path
            )

            metadata.chunk_count = chunk_count

            metadata.status = DocumentStatus.SUCCESS

            metadata.updated_at = datetime.utcnow()

            await self._firestore_service.update_document(
                metadata
            )

            return DocumentUploadResponse(
                filename=file.filename,
                chunks_indexed=chunk_count,
                message="Document uploaded and indexed successfully.",
            )

        except Exception as ex:

            metadata.status = DocumentStatus.FAILED

            metadata.last_error = str(ex)

            metadata.updated_at = datetime.utcnow()

            await self._firestore_service.update_document(
                metadata
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex),
            ) from ex

    async def list_documents(
        self,
    ) -> list[DocumentMetadata]:

        return await self._firestore_service.list_documents()

    async def get_document(
        self,
        document_id: str,
    ) -> DocumentMetadata | None:

        return await self._firestore_service.get_document(
            document_id
        )

    async def delete_document(
        self,
        document_id: str,
    ) -> None:

        await self._firestore_service.delete_document(
            document_id
        )