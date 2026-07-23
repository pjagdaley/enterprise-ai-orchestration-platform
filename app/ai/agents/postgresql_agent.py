"""
PostgreSQL Agent.
"""

from __future__ import annotations

import logging
from typing import Any

from app.ai.agents.base_agent import BaseAgent
from app.ai.models.parameters import PostgreSQLParameters
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse
from app.ai.tools.postgresql_tool import PostgreSQLTool

logger = logging.getLogger(__name__)


class PostgreSQLAgent(BaseAgent):
    """
    Agent responsible for PostgreSQL operations.
    """

    def __init__(
        self,
        tool: PostgreSQLTool,
    ) -> None:
        self._tool = tool

    @property
    def name(self) -> str:
        return "postgres"

    @property
    def description(self) -> str:
        return "Executes PostgreSQL database operations."

    async def execute(
        self,
        user_input: str,
        parameters: dict[str, Any],
    ) -> ToolResponse:
        """
        Execute a PostgreSQL operation.
        """

        logger.info(
            "PostgreSQL parameters received: %s",
            parameters,
        )

        params = PostgreSQLParameters.model_validate(parameters)

        logger.info(
            "Executing PostgreSQL operation='%s'",
            user_input,
        )

        return await self._tool.execute(
            ToolRequest(
                input=user_input,
                parameters=params.model_dump(),
            )
        )