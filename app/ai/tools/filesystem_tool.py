"""
MCP Tool.
"""

from app.ai.mcp.service import MCPService
from app.ai.tools.base_tool import BaseTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse


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
        return "mcp"

    @property
    def description(self) -> str:
        return "Executes tools exposed by an MCP server."

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute an MCP tool.

        request.input:
            MCP tool name

        request.parameters:
            MCP tool arguments
        """

        response = await self._mcp_service.execute_tool(
            tool_name=request.input,
            arguments=request.parameters,
        )

        return ToolResponse(
            success=response.success,
            result=response.data,
            error=response.error,
        )