"""
Planner Agent.

Determines how a user request should be processed.
"""

import logging
import re
from app.ai.agents.base_agent import BaseAgent
from app.ai.agents.models import SupervisorDecision
from app.ai.services.supervisor_service import SupervisorService

logger = logging.getLogger(__name__)


class SupervisorAgent(BaseAgent):

    def __init__(self):

        self._service = SupervisorService()

    async def decide(
        self,
        user_input: str,
        parameters: dict,
    ) -> SupervisorDecision:

        logger.info(
            "Supervisor received request: '%s'",
            user_input,
        )

        decision = await self._service.execute(
            user_input=user_input,
        )

        logger.info(
            "Supervisor decision: %s",
            decision,
        )

        return decision




    """
    def decide(
        self,
        user_input: str,
    ) -> SupervisorDecision:
       
        #Determine which agent should handle the request.
        

        user_input = user_input.strip()
        lower_input = user_input.lower()

        logger.info(
            "Supervisor received request: '%s'",
            user_input,
        )

        #
        # Calculator
        #
        if re.fullmatch(
            r"[0-9+\-*/().\s]+",
            user_input,
        ):
            logger.info(
                "Supervisor routed request to CalculatorAgent"
            )

            return SupervisorDecision(
                agent="calculator",
                input=user_input,
            )

        #
        # Filesystem - Read file
        #
        if lower_input.startswith("read "):
            path = user_input[5:].strip()

            logger.info(
                "Supervisor routed request to FilesystemAgent "
                "(tool=read_text_file, path=%s)",
                path,
            )

            return SupervisorDecision(
                agent="filesystem",
                input="read_text_file",
                parameters={
                    "path": path,
                },
            )

        #
        # Filesystem - List directory
        #
        if lower_input.startswith("list "):
            path = user_input[5:].strip()

            logger.info(
                "Supervisor routed request to FilesystemAgent "
                "(tool=list_directory, path=%s)",
                path,
            )

            return SupervisorDecision(
                agent="filesystem",
                input="list_directory",
                parameters={
                    "path": path,
                },
            )

        #
        # Filesystem - Create directory
        #
        if lower_input.startswith("mkdir "):
            path = user_input[6:].strip()

            logger.info(
                "Supervisor routed request to FilesystemAgent "
                "(tool=create_directory, path=%s)",
                path,
            )

            return SupervisorDecision(
                agent="filesystem",
                input="create_directory",
                parameters={
                    "path": path,
                },
            )

        #
        # Git - Status
        #
        if (
            lower_input == "git status"
            or lower_input == "show git status"
            or lower_input == "status"
        ):
            logger.info(
                "Supervisor routed request to GitAgent "
                "(tool=git_status)"
            )

            return SupervisorDecision(
                agent="git",
                input="git_status",
            )

        #
        # Git - Commit history
        #
        if (
            lower_input.startswith("git log")
            or "commit history" in lower_input
            or "show commits" in lower_input
            or "show last commits" in lower_input
        ):
            logger.info(
                "Supervisor routed request to GitAgent "
                "(tool=git_log)"
            )

            return SupervisorDecision(
                agent="git",
                input="git_log",
                parameters={
                    "max_count": 10,
                },
            )

        #
        # Git - Branches
        #
        if (
            lower_input == "git branch"
            or "branches" in lower_input
            or "list branches" in lower_input
        ):
            logger.info(
                "Supervisor routed request to GitAgent "
                "(tool=git_branch)"
            )

            return SupervisorDecision(
                agent="git",
                input="git_branch",
                parameters={
                    "branch_type": "local",
                },
            )

        #
        # Git - Unstaged changes
        #
        if (
            "git diff" in lower_input
            or "show diff" in lower_input
            or "unstaged" in lower_input
        ):
            logger.info(
                "Supervisor routed request to GitAgent "
                "(tool=git_diff_unstaged)"
            )

            return SupervisorDecision(
                agent="git",
                input="git_diff_unstaged",
                parameters={
                    "context_lines": 3,
                },
            )
        
        text = user_input.lower()

        #
        # PostgreSQL
        #
        if (
            "table" in text
            or "sql" in text
            or "database" in text
            or "postgres" in text
        ):

            logger.info(
                "Supervisor routed request to PostgreSQLAgent"
            )
            
            return SupervisorDecision(
                agent="postgres",
                input="query",
                parameters={},
            )

        #
        # Default -> RAG
        #
        logger.info(
            "Supervisor routed request to RAGAgent"
        )

        return SupervisorDecision(
            agent="rag",
            input=user_input,
        )"""