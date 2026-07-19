"""
Chat API endpoints.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Request

from app.application.services.chat_service import ChatService
from app.schemas.chat import ChatRequest
from app.schemas.chat import ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


def get_chat_service(
    request: Request,
) -> ChatService:

    return request.app.state.services.chat_service


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with the AI assistant",
    description="Send a message to the Enterprise AI Orchestration Platform.",
)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """
    Process a chat request.
    """

    response = await service.chat(request.message)

    return ChatResponse(
        response=response,
    )