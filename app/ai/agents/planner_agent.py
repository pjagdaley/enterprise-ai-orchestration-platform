"""
Planner Agent.

Determines how a user request should be processed.
"""

import re

from app.ai.agents.models import PlannerResponse


class PlannerAgent:
    """
    Determines the execution strategy for a user request.
    """

    def plan(
        self,
        user_input: str,
    ) -> PlannerResponse:
        """
        Determine which tool should handle the request.
        """

        user_input = user_input.strip()
        lower_input = user_input.lower()

        #
        # Calculator
        #

        if re.fullmatch(
            r"[0-9+\-*/().\s]+",
            user_input,
        ):
            return PlannerResponse(
                tool="calculator",
                input=user_input,
            )

        #
        # MCP - Read file
        #

        if lower_input.startswith("read "):
            path = user_input[5:].strip()

            return PlannerResponse(
                tool="mcp",
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

            return PlannerResponse(
                tool="mcp",
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

            return PlannerResponse(
                tool="mcp",
                input="create_directory",
                parameters={
                    "path": path,
                },
            )

        #
        # Default -> RAG
        #

        return PlannerResponse(
            tool="rag",
            input=user_input,
        )