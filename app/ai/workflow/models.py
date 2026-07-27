"""
Workflow domain models.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.ai.planner.models import ExecutionPlan


class WorkflowStatus(str, Enum):
    """
    Overall workflow status.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class StepStatus(str, Enum):
    """
    Workflow step status.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStepResult(BaseModel):
    """
    Result of a workflow step.
    """

    model_config = ConfigDict(extra="forbid")

    step_number: int

    status: StepStatus = StepStatus.PENDING

    output: Any | None = None

    error: str | None = None


class WorkflowExecution(BaseModel):
    """
    Represents a workflow execution.
    """

    model_config = ConfigDict(extra="forbid")

    execution_plan: ExecutionPlan

    status: WorkflowStatus = WorkflowStatus.PENDING

    results: list[WorkflowStepResult] = Field(
        default_factory=list,
    )