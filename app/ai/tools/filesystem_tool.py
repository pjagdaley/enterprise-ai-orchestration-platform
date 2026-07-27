"""
MCP Tool.
"""

from app.ai.mcp.service import MCPService
from app.ai.tools.base_tool import BaseTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse

import logging

logger = logging.getLogger(__name__)


class FilesystemTool(BaseTool):
    """
    AI tool that executes tools exposed by an MCP server.
    """

    def __init__(
        self,
        filesystem_mcp_service: MCPService,
    ) -> None:
        self._mcp_service = filesystem_mcp_service

    @property
    def name(self) -> str:
        return "filesystem"

    @property
    def description(self) -> str:
        return "Executes filesystem operations through the Filesystem MCP server.."

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute an MCP tool.

        request.action:
            MCP tool name

        request.parameters:
            MCP tool arguments
        """
        logger.info(
            "Executing filesystem action='%s' parameters=%s",
            request.action,
            request.parameters,
        )

        response = await self._mcp_service.execute_tool(
            tool_name=request.action,
            arguments=request.parameters,
        )

        logger.info(
            "Filesystem MCP response success=%s",
            response.success,
        )

        logger.info(
            "Filesystem MCP response data=%r",
            response.data,
        )

        logger.info(
            "Filesystem MCP response error=%r",
            response.error,
        )

        return ToolResponse(
            success=response.success,
            result=response.data,
            error=response.error,
        )