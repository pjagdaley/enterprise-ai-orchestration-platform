"""
Models used by AI agents.
"""

from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class PlannerResponse(BaseModel):
    """
    Execution plan returned by the Planner Agent.
    """

    model_config = ConfigDict(extra="forbid")

    tool: str = Field(
        ...,
        description="Selected tool name."
    )

    input: str = Field(
        ...,
        description="Primary input for the selected tool."
    )

    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional tool-specific parameters."
    )