"""
Test the SupervisorService.
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

from app.ai.services.supervisor_service import SupervisorService


async def main():

    supervisor = SupervisorService()

    user_request = (
        "Read employees.txt, summarize it and save the summary "
        "to summary.txt"
    )

    print("=" * 80)
    print("USER REQUEST")
    print("=" * 80)
    print(user_request)

    print()

    decision = await supervisor.decide(user_request)

    print("=" * 80)
    print("SUPERVISOR DECISION")
    print("=" * 80)

    print(f"Agent      : {decision.agent}")
    print(f"User Input : {decision.user_input}")
    print(f"Parameters : {decision.parameters}")


if __name__ == "__main__":
    asyncio.run(main())