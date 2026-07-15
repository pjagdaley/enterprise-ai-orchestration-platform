"""
Document API endpoints.
"""

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from starlette import status

from app.application.services.document_service import DocumentService
from app.schemas.document import DocumentUploadResponse
from app.schemas.firestore import DocumentMetadata

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentUploadResponse:
    """
    Upload and index a document.
    """

    return await document_service.upload_document(file)


@router.get(
    "",
    response_model=list[DocumentMetadata],
    status_code=status.HTTP_200_OK,
    summary="List all documents",
)
async def list_documents() -> list[DocumentMetadata]:
    """
    Return all indexed documents.
    """

    return await document_service.list_documents()


@router.get(
    "/{document_id}",
    response_model=DocumentMetadata,
    status_code=status.HTTP_200_OK,
    summary="Get document",
)
async def get_document(
    document_id: str,
) -> DocumentMetadata:
    """
    Return a document by id.
    """

    document = await document_service.get_document(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return document


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete document",
)
async def delete_document(
    document_id: str,
) -> None:
    """
    Delete a document.

    NOTE:
    Currently deletes only Firestore metadata.
    Qdrant vectors and uploaded files will be removed
    in a future implementation.
    """

    await document_service.delete_document(
        document_id
    )