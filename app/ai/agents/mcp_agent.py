"""
MCP Agent.
"""

from typing import Any

from app.ai.agents.base_agent import BaseAgent

from app.ai.tools.mcp_tool import MCPTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse

import logging
logger = logging.getLogger(__name__)


class MCPAgent(BaseAgent):
    """
    Executes MCP tools.
    """

    def __init__(
        self,
        tool: MCPTool,
    ) -> None:

        self._tool = tool

    @property
    def name(self) -> str:
        return "mcp"

    async def execute(
        self,
        user_input: str,
        parameters: dict[str, Any],
    ) -> ToolResponse:

        logger.info(
            "Executing MCP tool='%s' with parameters=%s",
            user_input,
            parameters,
        )
        
        return await self._tool.execute(
            ToolRequest(
                input=user_input,
                parameters=parameters,
            )
        )