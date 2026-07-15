"""
Document application service.
"""

import shutil
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException
from fastapi import UploadFile
from starlette import status

from app.domain.enums.source_type import DocumentSourceType
from app.domain.enums.document_status import DocumentStatus
from app.infrastructure.firestore.firestore_service import FirestoreService
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
        """
        Initialize the document service.
        """

        self._ingest_service = IngestService()
        self._firestore_service = FirestoreService()

        self._upload_dir = Path("uploads")
        self._upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def upload_document(
        self,
        file: UploadFile,
    ) -> DocumentUploadResponse:
        """
        Upload and ingest a document.
        """

        #
        # Validate file extension
        #

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {extension}",
            )

        #
        # Save uploaded file
        #

        destination = self._upload_dir / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        #
        # Create Firestore metadata
        #

        metadata = DocumentMetadata(
            document_id=str(uuid.uuid4()),
            source_path=str(destination),
            generation="1",
            extension=extension,
            content_type=file.content_type
            or "application/octet-stream",
            source_type=DocumentSourceType.LOCAL,
            status=DocumentStatus.PROCESSING,
            chunk_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_error=None,
        )

        await self._firestore_service.save_document(metadata)

        try:
            #
            # Ingest document
            #

            chunk_count = await self._ingest_service.ingest(
                str(destination)
            )

            print(f"Chunks created: {chunk_count}")

            #
            # Update Firestore metadata
            #

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
        """
        Return all indexed documents.
        """

        return await self._firestore_service.list_documents()

    async def get_document(
        self,
        document_id: str,
    ) -> DocumentMetadata | None:
        """
        Return a document by id.
        """

        return await self._firestore_service.get_document(
            document_id
        )

    async def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete a document.

        NOTE:
        Currently this removes only Firestore metadata.
        Qdrant vectors and uploaded files will be deleted
        in a later phase.
        """

        await self._firestore_service.delete_document(
            document_id
        )    