"""
Schemas for the Chat API.
"""

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """
    Chat request.
    """
    model_config = ConfigDict(extra="forbid")

    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="User message."
    )


class ChatResponse(BaseModel):
    """
    Chat response.
    """
    model_config = ConfigDict(extra="forbid")
    
    response: str = Field(
        ...,
        description="AI generated response."
    )