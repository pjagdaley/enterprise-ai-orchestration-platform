"""
Test the PlannerService.
"""

import asyncio
import sys
from pathlib import Path

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ai.planner.planner import Planner
from app.ai.planner.planner_service import PlannerService


async def main():

    planner = Planner()

    planner_service = PlannerService(
        planner=planner,
    )

    user_request = (
        "Read employees.txt, summarize it and save the summary "
        "to summary.txt"
    )

    print("=" * 80)
    print("USER REQUEST")
    print("=" * 80)
    print(user_request)

    print()

    response = await planner_service.create_plan(
        user_request,
    )

    print("=" * 80)
    print("PLAN TYPE")
    print("=" * 80)

    print(response.plan_type)

    print()

    print("=" * 80)
    print("REASONING")
    print("=" * 80)

    print(response.reasoning)

    print()

    print("=" * 80)
    print("WORKFLOW")
    print("=" * 80)

    for step in response.execution_plan.steps:

        print(f"Step       : {step.step_number}")
        print(f"Agent      : {step.agent}")
        print(f"Action     : {step.action}")
        print(f"Parameters : {step.parameters}")
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())