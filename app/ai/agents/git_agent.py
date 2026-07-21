"""
Git Agent.
"""

from typing import Any
import logging

from app.ai.agents.base_agent import BaseAgent
from app.ai.tools.git_tool import GitTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse

logger = logging.getLogger(__name__)


class GitAgent(BaseAgent):
    """
    AI Agent responsible for executing Git operations
    through the Git MCP server.
    """

    def __init__(
        self,
        tool: GitTool,
    ) -> None:
        self._tool = tool

    @property
    def name(self) -> str:
        return "git"

    @property
    def description(self) -> str:
        return (
            "Executes Git repository operations including status, "
            "commit, log, diff, branch, checkout, and staging."
        )

    async def execute(
        self,
        user_input: str,
        parameters: dict[str, Any],
    ) -> ToolResponse:
        """
        Execute a Git operation.

        Parameters
        ----------
        user_input:
            Git MCP tool name, for example:
                git_status
                git_log
                git_commit
                git_add
                git_branch
                git_checkout

        parameters:
            Parameters required by the Git MCP tool.
            Example:
                {
                    "message": "Initial commit"
                }
        """

        logger.info(
            "Executing Git tool '%s' with parameters=%s",
            user_input,
            parameters,
        )

        request = ToolRequest(
            input=user_input,
            parameters=parameters,
        )

        response = await self._tool.execute(request)

        logger.info(
            "Git tool '%s' completed successfully=%s",
            user_input,
            response.success,
        )

        return response