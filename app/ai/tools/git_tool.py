"""
Git Tool.
"""

import logging

from app.ai.mcp.service import MCPService
from app.ai.tools.base_tool import BaseTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse

logger = logging.getLogger(__name__)


class GitTool(BaseTool):
    """
    AI tool that executes Git operations exposed by the Git MCP server.
    """

    def __init__(
        self,
        git_mcp_service: MCPService,
        repo_path: str,
    ) -> None:
        self._mcp_service = git_mcp_service
        self._repo_path = repo_path

    @property
    def name(self) -> str:
        return "git"

    @property
    def description(self) -> str:
        return (
            "Provides Git repository operations including status, "
            "diff, commit, log, branch, checkout, and staging."
        )

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute a Git MCP tool.

        request.input:
            Git MCP tool name
            Examples:
                git_status
                git_log
                git_commit
                git_add
                git_branch

        request.parameters:
            Parameters required by the Git MCP tool.
            repo_path is automatically injected.
        """

        logger.info(
            "Executing Git MCP tool='%s' with parameters=%s",
            request.input,
            request.parameters,
        )

        # Copy parameters to avoid modifying the caller's dictionary
        arguments = dict(request.parameters or {})

        # Automatically provide repository path
        arguments["repo_path"] = self._repo_path

        response = await self._mcp_service.execute_tool(
            tool_name=request.input,
            arguments=arguments,
        )

        logger.info(
            "Git MCP response success=%s",
            response.success,
        )

        logger.info(
            "Git MCP response data=%r",
            response.data,
        )

        logger.info(
            "Git MCP response error=%r",
            response.error,
        )

        return ToolResponse(
            success=response.success,
            result=response.data,
            error=response.error,
        )