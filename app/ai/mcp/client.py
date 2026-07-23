"""
MCP Client implementation.
"""

from __future__ import annotations

import time

from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.ai.mcp.models import MCPResponse, MCPTool

import logging
logger = logging.getLogger(__name__)

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

        logger.info("Disconnecting MCP client...")

        start = time.perf_counter()

        await self._stack.aclose()

        elapsed = time.perf_counter() - start

        logger.info(
            "MCP client disconnected in %.2f seconds",
            elapsed,
        )

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

        logger.info("structuredContent=%r", result.structuredContent)
        logger.info("content=%r", result.content)
        logger.info("isError=%s", result.isError)
        
        data = None
        error = None

        if result.isError:

            if result.content:
                text_parts = [
                    item.text
                    for item in result.content
                    if hasattr(item, "text")
                ]
                error = "\n".join(text_parts)
            else:
                error = "Tool execution failed"

        else:

            #
            # Prefer structured content.
            #
            if result.structuredContent is not None:

                structured = result.structuredContent

                if (
                    isinstance(structured, dict)
                    and "content" in structured
                ):
                    data = structured["content"]
                else:
                    data = structured

            #
            # Otherwise use text content.
            #
            elif result.content:

                text_parts = [
                    item.text
                    for item in result.content
                    if hasattr(item, "text")
                ]

                data = "\n".join(text_parts)

        return MCPResponse(
            success=not result.isError,
            data=data,
            error=error,
        )