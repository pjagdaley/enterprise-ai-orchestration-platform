"""
Workflow Executor test.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.bootstrap.services import ApplicationServices
from app.ai.planner.models import (
    ExecutionPlan,
    WorkflowStep,
)
from app.ai.workflow.context import WorkflowContext
from app.ai.workflow.executor import WorkflowExecutor
from app.ai.workflow.models import WorkflowExecution


async def main() -> None:

    services = ApplicationServices()

    await services.initialize()

    try:

        plan = ExecutionPlan(
            steps=[
                WorkflowStep(
                    step_number=1,
                    agent="calculator",
                    action="",
                    parameters={
                        "expression": "2 + 3 * 10"
                    },
                ),
            ]
        )

        execution = WorkflowExecution(
            execution_plan=plan,
        )

        executor = WorkflowExecutor(
            services.agent_registry,
        )

        context = WorkflowContext()

        result = await executor.execute(
            execution=execution,
            context=context,
        )

        print("=" * 80)
        print("WORKFLOW STATUS")
        print("=" * 80)

        print(result.status)

        print()

        for step in result.results:

            print(f"Step      : {step.step_number}")
            print(f"Status    : {step.status}")
            print(f"Output    : {step.output}")
            print(f"Error     : {step.error}")
            print("-" * 80)

        print()

        print("=" * 80)
        print("WORKFLOW CONTEXT")
        print("=" * 80)

        print(context.as_dict())

    finally:

        await services.shutdown()


if __name__ == "__main__":
    asyncio.run(main())