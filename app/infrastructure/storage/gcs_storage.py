"""
Google Cloud Storage implementation.
"""

from fastapi import UploadFile
from google.cloud import storage

from app.core.config import settings
from app.infrastructure.storage.base_storage import BaseStorage


class GCSStorage(BaseStorage):
    """
    Google Cloud Storage implementation.
    """

    def __init__(self) -> None:

        self._client = storage.Client(
            project=settings.project_id,
        )

        self._bucket = self._client.bucket(
            settings.gcs_bucket,
        )

    async def upload(
        self,
        file: UploadFile,
    ) -> str:
        """
        Upload a file to Google Cloud Storage.

        Returns:
            GCS object path.
        """

        blob = self._bucket.blob(file.filename)

        blob.upload_from_file(
            file.file,
            content_type=file.content_type,
        )

        return f"gs://{settings.gcs_bucket}/{file.filename}"

    async def delete(
        self,
        storage_path: str,
    ) -> None:
        """
        Delete a document from Google Cloud Storage.
        """

        prefix = f"gs://{settings.gcs_bucket}/"

        object_name = storage_path.replace(
            prefix,
            "",
        )

        blob = self._bucket.blob(
            object_name,
        )

        blob.delete()