"""
MCP Agent.
"""

from typing import Any

from app.ai.agents.base_agent import BaseAgent

from app.ai.models.parameters import FilesystemParameters
from app.ai.tools.filesystem_tool import FilesystemTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse

import logging
logger = logging.getLogger(__name__)


class FilesystemAgent(BaseAgent):
    """
    Executes MCP tools.
    """

    def __init__(
        self,
        tool: FilesystemTool,
    ) -> None:

        self._tool = tool

    @property
    def name(self) -> str:
        return "filesystem"

    async def execute(
    self,
    user_input: str,
    parameters: dict[str, Any],
    ) -> ToolResponse:

        logger.info("Filesystem parameters received: %s", parameters)

        params = FilesystemParameters.model_validate(parameters)
               
        logger.info(
            "Executing filesystem action='%s'",
            user_input,
        )

        return await self._tool.execute(
            ToolRequest(
                action=user_input,
                parameters=params.model_dump(),
            )
        )