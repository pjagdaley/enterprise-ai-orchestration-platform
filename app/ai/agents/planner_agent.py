"""
Planner Agent.

Determines how a user request should be processed.
"""

import re


class PlannerAgent:
    """
    Determines the execution strategy for a user request.
    """

    def plan(
        self,
        user_input: str,
    ) -> str:
        """
        Determine which component should handle the request.

        Returns:
            calculator
            llm
            rag (future)
            mcp (future)
        """

        #
        # Calculator
        #

        if re.fullmatch(
            r"[0-9+\-*/().\s]+",
            user_input,
        ):
            return "calculator"

        #
        # Future RAG
        #
        return "rag"

        # if ...

        #
        # Future MCP
        #

        # if ...

        #
        # Default
        #

        #return "llm"