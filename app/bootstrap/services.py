"""
Application services.

Responsible for creating, initializing, and shutting down
shared application services.
"""

from app.ai.agents.calculator_agent import CalculatorAgent
from app.ai.agents.mcp_agent import MCPAgent
from app.ai.agents.rag_agent import RAGAgent
from app.ai.agents.registry import AgentRegistry
from app.ai.mcp.service import MCPService
from app.ai.orchestrator.graph import WorkflowGraph
from app.ai.tools.mcp_tool import MCPTool
from app.application.services.chat_service import ChatService


class ApplicationServices:
    """
    Holds all shared application services.
    """

    def __init__(self) -> None:
        self.mcp_service: MCPService | None = None
        self.agent_registry: AgentRegistry | None = None
        self.workflow: WorkflowGraph | None = None
        self.chat_service: ChatService | None = None

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
        # Agent Registry
        #
        self.agent_registry = AgentRegistry()

        self.agent_registry.register(
            RAGAgent()
        )

        self.agent_registry.register(
            CalculatorAgent()
        )

        self.agent_registry.register(
            MCPAgent(
                MCPTool(self.mcp_service)
            )
        )

        #
        # Workflow
        #
        self.workflow = WorkflowGraph(
            agent_registry=self.agent_registry
        )

        #
        # Chat Service
        #
        self.chat_service = ChatService(
            self.workflow
        )

    async def shutdown(self) -> None:
        """
        Shutdown application services.
        """

        if self.mcp_service:
            await self.mcp_service.shutdown()