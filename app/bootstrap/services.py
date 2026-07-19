"""
Application services.

Responsible for creating, initializing, and shutting down
shared application services.
"""

from app.ai.mcp.service import MCPService
from app.ai.orchestrator.graph import WorkflowGraph
from app.ai.tools.calculator_tool import CalculatorTool
from app.ai.tools.mcp_tool import MCPTool
from app.ai.tools.rag_tool import RAGTool
from app.ai.tools.registry import ToolRegistry
from app.application.services.chat_service import ChatService


class ApplicationServices:
    """
    Holds all shared application services.
    """

    def __init__(self) -> None:
        self.mcp_service: MCPService | None = None
        self.tool_registry: ToolRegistry | None = None

    async def initialize(self) -> None:
        """
        Initialize all application services.
        """

        #
        # MCP Service
        #
        self.mcp_service = MCPService(
            command="npx",
            args=[
                "@modelcontextprotocol/server-filesystem",
                r"C:\Temp",
            ],
        )

        await self.mcp_service.initialize()

        #
        # Tool Registry
        #
        self.tool_registry = ToolRegistry()

        self.tool_registry.register(CalculatorTool())
        self.tool_registry.register(RAGTool())
        self.tool_registry.register(
            MCPTool(self.mcp_service)
        )

        self.workflow = WorkflowGraph(
            self.tool_registry
        )

        self.chat_service = ChatService(
            self.workflow
        )

    async def shutdown(self) -> None:
        """
        Shutdown application services.
        """

        if self.mcp_service:
            await self.mcp_service.shutdown()