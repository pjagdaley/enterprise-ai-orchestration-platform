"""
Workflow executor.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from app.ai.agents.registry import AgentRegistry
from app.ai.workflow.context import WorkflowContext
from app.ai.workflow.models import (
    StepStatus,
    WorkflowExecution,
    WorkflowStatus,
    WorkflowStepResult,
)

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """
    Executes workflow plans sequentially.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
    ) -> None:
        self._agent_registry = agent_registry

    async def execute(
        self,
        execution: WorkflowExecution,
        context: WorkflowContext,
    ) -> WorkflowExecution:
        """
        Execute a workflow.
        """

        logger.info(
            "Starting workflow execution (%d steps).",
            len(execution.execution_plan.steps),
        )

        execution.status = WorkflowStatus.RUNNING

        for step in execution.execution_plan.steps:

            context.current_step = step.step_number

            logger.info(
                "Executing step=%d agent='%s' action='%s'",
                step.step_number,
                step.agent,
                step.action,
            )

            result = WorkflowStepResult(
                step_number=step.step_number,
                status=StepStatus.RUNNING,
            )

            execution.results.append(result)

            start_time = time.perf_counter()

            try:

                #
                # Resolve workflow variables.
                #
                resolved_parameters = self._resolve_parameters(
                    step.parameters,
                    context,
                )

                #
                # Get the agent.
                #
                agent = self._agent_registry.get(step.agent)

                #
                # Execute the step.
                #
                output = await agent.execute(
                    user_input=step.action,
                    parameters=resolved_parameters,
                )

                duration_ms = round(
                    (time.perf_counter() - start_time) * 1000,
                    2,
                )

                #
                # Record successful execution.
                #
                result.status = StepStatus.COMPLETED
                result.output = output

                #
                # Optional:
                # if WorkflowStepResult has duration_ms
                #
                # result.duration_ms = duration_ms

                #
                # Store the complete ToolResponse.
                #
                context.set(
                    f"step_{step.step_number}",
                    output,
                )

                #
                # Convenience aliases.
                #
                context.set(
                    f"step_{step.step_number}_output",
                    output.result,
                )

                context.set(
                    f"step_{step.step_number}_success",
                    output.success,
                )

                context.set(
                    f"step_{step.step_number}_error",
                    output.error,
                )

                logger.info(
                    "Completed step=%d in %.2f ms",
                    step.step_number,
                    duration_ms,
                )

            except Exception as ex:

                duration_ms = round(
                    (time.perf_counter() - start_time) * 1000,
                    2,
                )

                result.status = StepStatus.FAILED
                result.error = str(ex)

                #
                # Optional:
                # result.duration_ms = duration_ms
                #

                execution.status = WorkflowStatus.FAILED

                logger.exception(
                    "Workflow failed at step=%d after %.2f ms",
                    step.step_number,
                    duration_ms,
                )

                return execution

        execution.status = WorkflowStatus.COMPLETED

        logger.info("Workflow execution completed successfully.")

        return execution

    def _resolve_parameters(
        self,
        parameters: dict[str, Any],
        context: WorkflowContext,
    ) -> dict[str, Any]:
        """
        Resolve workflow variables.

        Example:

            "{{step_1_output}}"

        becomes

            context.get("step_1_output")
        """

        return {
            key: self._resolve_value(value, context)
            for key, value in parameters.items()
        }

    def _resolve_value(
        self,
        value: Any,
        context: WorkflowContext,
    ) -> Any:
        """
        Recursively resolve workflow variables.
        """

        #
        # Resolve workflow variables.
        #
        if isinstance(value, str):

            if value.startswith("{{") and value.endswith("}}"):

                variable = value[2:-2].strip()

                resolved = context.get(variable)

                if resolved is None:
                    raise ValueError(
                        f"Workflow variable '{variable}' not found."
                    )

                return resolved

            return value

        #
        # Resolve dictionaries.
        #
        if isinstance(value, dict):

            return {
                k: self._resolve_value(v, context)
                for k, v in value.items()
            }

        #
        # Resolve lists.
        #
        if isinstance(value, list):

            return [
                self._resolve_value(item, context)
                for item in value
            ]

        #
        # Primitive values.
        #
        return value