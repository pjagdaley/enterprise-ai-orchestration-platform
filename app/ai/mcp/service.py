"""
MCP Service.
"""

from __future__ import annotations

from app.ai.mcp.client import MCPClient
from app.ai.mcp.models import MCPResponse, MCPTool


class MCPService:
    """
    High-level service for interacting with MCP servers.
    """

    def __init__(
        self,
        command: str,
        args: list[str],
        env: dict[str, str] | None = None,
    ) -> None:

        self._client = MCPClient(
            command=command,
            args=args,
            env=env,
        )

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected

    async def initialize(self) -> None:
        """
        Initialize the MCP client.
        """

        if not self.is_connected:
            await self._client.connect()

    async def shutdown(self) -> None:
        """
        Shutdown the MCP client.
        """

        if self.is_connected:
            await self._client.disconnect()

    async def list_tools(self) -> list[MCPTool]:
        """
        Return all available MCP tools.
        """

        return await self._client.list_tools()

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> MCPResponse:
        """
        Execute an MCP tool.
        """

        return await self._client.call_tool(
            tool_name,
            arguments,
        )