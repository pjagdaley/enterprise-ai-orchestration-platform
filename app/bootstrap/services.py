"""
Application services.

Responsible for creating, initializing, and shutting down
shared application services.
"""

from venv import logger

from app.ai.agents.calculator_agent import CalculatorAgent
from app.ai.agents.filesystem_agent import FilesystemAgent
from app.ai.agents.postgresql_agent import PostgreSQLAgent
from app.ai.agents.rag_agent import RAGAgent
from app.ai.agents.git_agent import GitAgent
from app.ai.agents.registry import AgentRegistry
from app.ai.mcp.service import MCPService
from app.ai.orchestrator.graph import WorkflowGraph
from app.ai.tools.filesystem_tool import FilesystemTool
from app.ai.tools.git_tool import GitTool
from app.ai.tools.postgresql_tool import PostgreSQLTool
from app.application.services.chat_service import ChatService
from app.domain import tools


class ApplicationServices:
    """
    Holds all shared application services.
    """

    def __init__(self) -> None:
        self.filesystem_mcp_service: MCPService | None = None
        self.git_mcp_service: MCPService | None = None
        self.postgres_mcp_service: MCPService | None = None
        self.agent_registry: AgentRegistry | None = None
        self.workflow: WorkflowGraph | None = None
        self.chat_service: ChatService | None = None

    async def initialize(self) -> None:
        """
        Initialize all application services.
        """

        #
        # Filesystem MCP
        #
        self.filesystem_mcp_service = MCPService(
            command="npx",
            args=[
                "@modelcontextprotocol/server-filesystem",
                r"C:\Temp",
            ],
        )

        await self.filesystem_mcp_service.initialize()

        #
        # Git MCP
        #
        self.git_mcp_service = MCPService(
            command="uvx",
            args=[
                "mcp-server-git",
                "--repository",
                r"C:\AI-ML-Projects\enterprise-ai-orchestration-platform",
            ],
        )

        await self.git_mcp_service.initialize()

        #
        # PostgreSQL MCP
        #
        # self.postgres_mcp_service = MCPService(
        #     command="...",
        #     args=[...],
        # )
        #
        # await self.postgres_mcp_service.initialize()
        self.postgres_mcp_service = MCPService(
            command="npx",
            args=[
                "@modelcontextprotocol/server-postgres",
                "postgresql://postgres:postgres@localhost:5432/enterprise_ai",
            ],
        )

        await self.postgres_mcp_service.initialize()

        tools = await self.postgres_mcp_service.list_tools()

        logger.info("PostgreSQL MCP Tools: %s", tools)

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
            FilesystemAgent(
                FilesystemTool(
                    self.filesystem_mcp_service
                )
            )
        )

        git_tool = GitTool(
            git_mcp_service=self.git_mcp_service,
            repo_path=r"C:\AI-ML-Projects\enterprise-ai-orchestration-platform",
        )

        self.agent_registry.register(
            GitAgent(
                git_tool
            )
        )

        postgres_tool = PostgreSQLTool(
            postgres_mcp_service=self.postgres_mcp_service,
        )

        postgres_agent = PostgreSQLAgent(
            tool=postgres_tool,
        )

        self.agent_registry.register(postgres_agent)

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

        if self.filesystem_mcp_service:
            await self.filesystem_mcp_service.shutdown()

        if self.git_mcp_service:
            await self.git_mcp_service.shutdown()