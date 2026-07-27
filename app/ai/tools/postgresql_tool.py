"""
PostgreSQL Tool.
"""

from __future__ import annotations

import logging

from app.ai.mcp.service import MCPService
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse
from app.ai.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)


class PostgreSQLTool(BaseTool):
    """
    Tool responsible for executing PostgreSQL MCP tools.
    """

    @property
    def name(self) -> str:
        return "postgres"

    @property
    def description(self) -> str:
        return "Performs PostgreSQL database operations."

    def __init__(
        self,
        postgres_mcp_service: MCPService,
    ) -> None:
        """
        Initialize the PostgreSQL tool.
        """

        self._mcp_service = postgres_mcp_service

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute a PostgreSQL MCP tool.
        """

        logger.info(
            "Executing PostgreSQL action='%s' parameters=%s",
            request.action,
            request.parameters,
        )

        response = await self._mcp_service.execute_tool(
            tool_name=request.action,
            arguments=request.parameters or {},
        )

        logger.info(
            "PostgreSQL MCP response success=%s",
            response.success,
        )

        logger.info(
            "PostgreSQL MCP response data=%r",
            response.data,
        )

        logger.info(
            "PostgreSQL MCP response error=%r",
            response.error,
        )

        return ToolResponse(
            success=response.success,
            result=response.data,
            error=response.error,
        )