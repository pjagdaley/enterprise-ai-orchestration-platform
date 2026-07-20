"""
Calculator Agent.
"""

from app.ai.agents.base_agent import BaseAgent

from app.ai.tools.calculator_tool import CalculatorTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse
from typing import Any

import logging
logger = logging.getLogger(__name__)


class CalculatorAgent(BaseAgent):
    """
    Executes calculator operations.
    """

    def __init__(self) -> None:
        self._tool = CalculatorTool()

    @property
    def name(self) -> str:
        return "calculator"

    async def execute(
    self,
    user_input: str,
    parameters: dict[str, Any],
    ) -> ToolResponse:

        logger.info(
            "Executing calculator expression='%s'",
            user_input,
        )
        
        return await self._tool.execute(
            ToolRequest(
                input=user_input,
                parameters=parameters,
            )
        )