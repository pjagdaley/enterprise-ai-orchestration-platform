"""
Base storage abstraction.
"""

from abc import ABC
from abc import abstractmethod

from fastapi import UploadFile


class BaseStorage(ABC):
    """
    Abstract base class for document storage.
    """

    @abstractmethod
    async def upload(
        self,
        file: UploadFile,
    ) -> str:
        """
        Upload a document.

        Args:
            file:
                Uploaded file.

        Returns:
            Storage path of the uploaded document.
        """
        pass

    @abstractmethod
    async def delete(
        self,
        storage_path: str,
    ) -> None:
        """
        Delete a stored document.

        Args:
            storage_path:
                Path of the stored document.
        """
        pass