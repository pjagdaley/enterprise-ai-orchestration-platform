"""
Firestore service for document metadata.
"""

from datetime import datetime

from app.infrastructure.firestore.client import FirestoreProvider
from app.schemas.firestore import DocumentMetadata


class FirestoreService:
    """
    Service responsible for persisting document metadata.
    """

    COLLECTION_NAME = "documents"

    def __init__(self) -> None:
        self._db = FirestoreProvider.get_client()

    async def save_document(
        self,
        metadata: DocumentMetadata,
    ) -> None:
        """
        Save document metadata.
        """

        (
            self._db.collection(self.COLLECTION_NAME)
            .document(metadata.document_id)
            .set(metadata.model_dump(mode="json"))
        )

    async def get_document(
        self,
        document_id: str,
    ) -> DocumentMetadata | None:
        """
        Retrieve a document by its document id.
        """

        document = (
            self._db.collection(self.COLLECTION_NAME)
            .document(document_id)
            .get()
        )

        if not document.exists:
            return None

        return DocumentMetadata(**document.to_dict())

    async def list_documents(
        self,
    ) -> list[DocumentMetadata]:
        """
        Retrieve all indexed documents.
        """

        documents: list[DocumentMetadata] = []

        for document in (
            self._db.collection(self.COLLECTION_NAME).stream()
        ):
            documents.append(
                DocumentMetadata(**document.to_dict())
            )

        return documents

    async def update_document(
        self,
        metadata: DocumentMetadata,
    ) -> None:
        """
        Update an existing document.
        """

        metadata.updated_at = datetime.utcnow()

        (
            self._db.collection(self.COLLECTION_NAME)
            .document(metadata.document_id)
            .set(
                metadata.model_dump(mode="json"),
                merge=True,
            )
        )

    async def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete a document.
        """

        (
            self._db.collection(self.COLLECTION_NAME)
            .document(document_id)
            .delete()
        )

    async def exists(
        self,
        document_id: str,
    ) -> bool:
        """
        Check whether a document exists.
        """

        document = (
            self._db.collection(self.COLLECTION_NAME)
            .document(document_id)
            .get()
        )

        return document.exists