"""
Common request and response models for LLM providers.
"""

from typing import Any

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    """
    Request sent to an LLM provider.
    """

    prompt: str = Field(
        ...,
        description="Input prompt."
    )

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="Sampling temperature."
    )

    max_tokens: int = Field(
        default=2048,
        gt=0,
        description="Maximum number of output tokens."
    )

    top_p: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="Top-p sampling."
    )    


class LLMResponse(BaseModel):
    """
    Response returned by an LLM provider.
    """

    content: str = Field(
        ...,
        description="Generated text."
    )

    model: str = Field(
        ...,
        description="Model used to generate the response."
    )

    finish_reason: str = Field(
        default="STOP",
        description="Reason generation finished."
    )

    prompt_tokens: int = Field(
        default=0,
        description="Number of prompt tokens."
    )

    completion_tokens: int = Field(
        default=0,
        description="Number of generated tokens."
    )

    total_tokens: int = Field(
        default=0,
        description="Total tokens consumed."
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific metadata."
    )