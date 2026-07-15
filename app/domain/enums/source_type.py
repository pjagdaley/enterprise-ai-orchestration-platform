from enum import Enum


class DocumentSourceType(str, Enum):
    LOCAL = "LOCAL"
    GCS = "GCS"
    ONEDRIVE = "ONEDRIVE"
    SHAREPOINT = "SHAREPOINT"
    S3 = "S3"