"""
Planner Agent.

Determines how a user request should be processed.
"""

import re

from app.ai.agents.models import SupervisorDecision

import logging

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Determines the execution strategy for a user request.
    """

    def decide(
        self,
        user_input: str,
    ) -> SupervisorDecision:
        """
        Determine which agent should handle the request.
        """

        user_input = user_input.strip()
        lower_input = user_input.lower()
        logger.debug(
            "Analyzing user request: %s",
            user_input,
        )

        #
        # Calculator
        #

        if re.fullmatch(
            r"[0-9+\-*/().\s]+",
            user_input,
        ):
            # Mathematical expressions
            logger.info(
                "Identified mathematical expression: %s",
                user_input,
            )
            return SupervisorDecision(
                agent="calculator",
                input=user_input,
            )

        #
        # MCP - Read file
        #

        if lower_input.startswith("read "):
            path = user_input[5:].strip()
            logger.info(
                "Identified file read request: %s",
                path,
            )

            return SupervisorDecision(
                agent="mcp",
                input="read_text_file",
                parameters={
                    "path": path,
                },
            )

        #
        # MCP - List directory
        #

        if lower_input.startswith("list "):
            path = user_input[5:].strip()

            logger.info(
                "Identified directory listing request: %s",
                path,
            )
            return SupervisorDecision(
                agent="mcp",
                input="list_directory",
                parameters={
                    "path": path,
                },
            )

        #
        # MCP - Create directory
        #

        if lower_input.startswith("mkdir "):
            path = user_input[6:].strip()

            
            logger.info(
                "Identified directory creation request: %s",
                path,
            )
            return SupervisorDecision(
                agent="mcp",
                input="create_directory",
                parameters={
                    "path": path,
                },
            )

        #
        # Default -> RAG
        #
        logger.info(
            "Defaulting to RAG agent for request: %s",
            user_input,
        )
        
        return SupervisorDecision(
            agent="rag",
            input=user_input,
        )