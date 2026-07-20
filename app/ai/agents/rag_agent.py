"""
RAG Agent.
"""

from app.ai.agents.base_agent import BaseAgent

from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse
from app.ai.tools.rag_tool import RAGTool
from typing import Any

import logging
logger = logging.getLogger(__name__)

class RAGAgent(BaseAgent):
    """
    Executes RAG searches.
    """

    def __init__(self) -> None:
        self._tool = RAGTool()

    @property
    def name(self) -> str:
        return "rag"

    async def execute(
        self,
        user_input: str,
        parameters: dict[str, Any],
    ) -> ToolResponse:
        
        logger.info(
            "Executing RAG agent"
        )

        return await self._tool.execute(
            ToolRequest(
                input=user_input,
                parameters=parameters,
            )
        )    