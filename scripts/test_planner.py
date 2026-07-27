"""
Test Planner.

Run:

python tests/test_planner.py

from any directory.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path


# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from app.ai.llm.factory import LLMFactory
from app.ai.planner.planner import Planner
from app.ai.planner.parser import PlannerParser


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

async def main() -> None:
    """
    Test Planner.
    """

    planner = Planner(LLMFactory())

    user_request = (
        "Read employees.txt, summarize the contents, "
        "and save the summary into summary.txt."
    )

    print("=" * 80)
    print("USER REQUEST")
    print("=" * 80)
    print(user_request)

    print("\nGenerating execution plan...\n")

    raw_response = await planner.plan(user_request)

    print("=" * 80)
    print("RAW LLM RESPONSE")
    print("=" * 80)
    print(raw_response)

    print("\nParsing response...\n")

    plan = PlannerParser.parse(raw_response)

    print("=" * 80)
    print("PLANNER RESPONSE")
    print("=" * 80)

    print(f"Plan Type : {plan.plan_type}")
    print(f"Reasoning : {plan.reasoning}")

    print("\nWorkflow Steps\n")

    for step in plan.execution_plan.steps:

        print(f"Step       : {step.step_number}")
        print(f"Agent      : {step.agent}")
        print(f"Input      : {step.input}")
        print(f"Parameters : {step.parameters}")
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())