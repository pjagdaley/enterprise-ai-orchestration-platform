"""
MCP Client implementation.
"""

from __future__ import annotations

from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.ai.mcp.models import MCPResponse, MCPTool


class MCPClient:
    """
    Wrapper around the official MCP Python SDK.
    """

    def __init__(
        self,
        command: str,
        args: list[str],
        env: dict[str, str] | None = None,
    ) -> None:

        self._server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env,
        )

        self._stack = AsyncExitStack()

        self._session: ClientSession | None = None

    async def connect(self) -> None:
        """
        Start the MCP server and initialize a session.
        """

        read_stream, write_stream = await self._stack.enter_async_context(
            stdio_client(self._server_params)
        )

        self._session = await self._stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await self._session.initialize()

    async def disconnect(self) -> None:
        """
        Close the MCP session.
        """

        await self._stack.aclose()

        self._session = None

    @property
    def is_connected(self) -> bool:
        return self._session is not None

    async def list_tools(self) -> list[MCPTool]:

        if self._session is None:
            raise RuntimeError("MCP client is not connected.")

        response = await self._session.list_tools()

        return [
            MCPTool(
                name=tool.name,
                description=tool.description,
                input_schema=tool.inputSchema or {},
            )
            for tool in response.tools
        ]

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> MCPResponse:

        if self._session is None:
            raise RuntimeError("MCP client is not connected.")

        result = await self._session.call_tool(
            tool_name,
            arguments=arguments,
        ) 

        data = None

        # Prefer structured data
        # Prefer structured data
        if result.structuredContent:

            structured = result.structuredContent

            # If the MCP server returns {"content": "..."},
            # extract the text so the rest of the application
            # always receives a string.
            if (
                isinstance(structured, dict)
                and "content" in structured
            ):
                data = structured["content"]
            else:
                data = structured

        error = None

        if result.isError:
            if result.content and hasattr(result.content[0], "text"):
                error = result.content[0].text
            else:
                error = "Tool execution failed"
        
        return MCPResponse(
            success=not result.isError,
            data=data,
            error=error,
        )