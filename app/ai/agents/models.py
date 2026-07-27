"""
Models used by AI agents.
"""

from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class SupervisorDecision(BaseModel):
    """
    Execution plan returned by the Planner Agent.
    """

    model_config = ConfigDict(extra="forbid")

    agent: str = Field(
        ...,
        description="Selected agent name."
    )

    user_input: str = Field(
        ...,
        description="Primary action for the selected agent."
    )

    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional agent-specific parameters."
    )