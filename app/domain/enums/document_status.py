"""
Document ingestion status.
"""

from enum import Enum


class DocumentStatus(str, Enum):
    """
    Status of a document during the ingestion lifecycle.
    """

    PENDING = "PENDING"

    PROCESSING = "PROCESSING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    DELETED = "DELETED"