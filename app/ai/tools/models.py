"""
Models used by AI tools.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ToolRequest(BaseModel):
    """
    Request sent to a tool.
    """

    model_config = ConfigDict(extra="forbid")

    input: str = Field(
        ...,
        description="Tool input."
    )

    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional tool parameters."
    )


class ToolResponse(BaseModel):
    """
    Response returned by a tool.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(
        ...,
        description="Whether the tool executed successfully."
    )

    result: str = Field(
        ...,
        description="Tool execution result."
    )