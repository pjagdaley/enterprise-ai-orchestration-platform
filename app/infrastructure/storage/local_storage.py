"""
Local file storage implementation.
"""

import shutil
from pathlib import Path

from fastapi import UploadFile

from app.infrastructure.storage.base_storage import BaseStorage


class LocalStorage(BaseStorage):
    """
    Stores uploaded documents on the local file system.
    """

    def __init__(
        self,
        upload_directory: str = "uploads",
    ) -> None:

        self._upload_dir = Path(upload_directory)

        self._upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def upload(
        self,
        file: UploadFile,
    ) -> str:
        """
        Save a document locally.

        Returns:
            Full storage path.
        """

        destination = self._upload_dir / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return str(destination)

    async def delete(
        self,
        storage_path: str,
    ) -> None:
        """
        Delete a locally stored document.
        """

        path = Path(storage_path)

        if path.exists():
            path.unlink()