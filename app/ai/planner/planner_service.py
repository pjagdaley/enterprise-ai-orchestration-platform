"""
Planner service.
"""

from .models import PlannerResponse
from .planner import Planner


class PlannerService:
    """
    Planner service.
    """

    def __init__(
        self,
        planner: Planner,
    ) -> None:
        self._planner = planner

    async def create_plan(
        self,
        user_request: str,
    ) -> PlannerResponse:
        """
        Create a validated execution plan.
        """

        return await self._planner.plan(user_request)