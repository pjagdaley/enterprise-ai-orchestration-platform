"""
Git Agent.
"""

from typing import Any
import logging

from app.ai.agents.base_agent import BaseAgent
from app.ai.models.parameters import GitParameters
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
        """

        logger.info(
            "Git parameters received: %s",
            parameters,
        )

        params = GitParameters.model_validate(parameters)

        logger.info(
            "Executing Git operation='%s'",
            user_input,
        )

        return await self._tool.execute(
            ToolRequest(
                action=user_input,
                parameters=params.model_dump(),
            )
        )