"""
PostgreSQL Agent.
"""

from __future__ import annotations

import logging

from app.ai.agents.base_agent import BaseAgent
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
        parameters: dict,
    ) -> ToolResponse:
        """
        Execute a PostgreSQL tool.
        """

        logger.info(
            "Executing PostgreSQL tool '%s' with parameters=%s",
            user_input,
            parameters,
        )

        request = ToolRequest(
            input="query",
            parameters={
                "sql": """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public';
                """
            },
        )

        response = await self._tool.execute(request)

        logger.info(
            "PostgreSQL tool '%s' completed successfully=%s",
            user_input,
            response.success,
        )

        return response