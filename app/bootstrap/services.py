"""
Application services.

Responsible for creating, initializing, and shutting down
shared application services.
"""

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

from app.ai.services.supervisor_service import SupervisorService
from app.ai.planner.planner import Planner
from app.ai.planner.planner_service import PlannerService
from app.ai.workflow.workflow_service import WorkflowService


from app.core.logging.logger import get_logger
logger = get_logger(__name__)

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

        self.supervisor_service: SupervisorService | None = None
        self.planner_service: PlannerService | None = None
        self.workflow_service: WorkflowService | None = None

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
                r"C:\AI-ML-Projects",
            ],
        )

        await self.filesystem_mcp_service.initialize()

        #tools = await self.filesystem_mcp_service.list_tools()
        #logger.info("Filesystem MCP Tools: %s", tools)

        #
        # Git MCP
        #        
        self.git_mcp_service = MCPService(
            command="uvx",
            args=[
                "--with",
                "mcp==1.28.1",
                "--with",
                "mcp-server-git",
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

        #tools = await self.postgres_mcp_service.list_tools()

        #logger.info("PostgreSQL MCP Tools: %s", tools)

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
        # Supervisor Service
        #
        self.supervisor_service = SupervisorService()

        #
        # Planner Service
        #
        planner = Planner()

        self.planner_service = PlannerService(
            planner=planner,
        )

        #
        # Workflow Service
        #
        self.workflow_service = WorkflowService(
            agent_registry=self.agent_registry,
        )

        #
        # Workflow
        #
        self.workflow = WorkflowGraph(
            agent_registry=self.agent_registry,
            supervisor_service=self.supervisor_service,
            planner_service=self.planner_service,
            workflow_service=self.workflow_service,
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
            logger.info("Stopping Filesystem MCP...")
            await self.filesystem_mcp_service.shutdown()
            logger.info("Filesystem MCP stopped.")

        if self.git_mcp_service:
            logger.info("Stopping Git MCP...")
            await self.git_mcp_service.shutdown()
            logger.info("Git MCP stopped.")

        if self.postgres_mcp_service:
            logger.info("Stopping PostgreSQL MCP...")
            await self.postgres_mcp_service.shutdown()
            logger.info("PostgreSQL MCP stopped.")