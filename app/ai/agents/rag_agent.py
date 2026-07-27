"""
RAG Agent.
"""

from typing import Any
import logging

from app.ai.agents.base_agent import BaseAgent
from app.ai.models.parameters import RAGParameters
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse
from app.ai.tools.rag_tool import RAGTool

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
            "RAG parameters received: %s",
            parameters,
        )

        params = RAGParameters.model_validate(parameters)

        logger.info(
            "Executing RAG search for query='%s'",
            user_input,
        )

        return await self._tool.execute(
            ToolRequest(
                action=user_input,
                parameters=params.model_dump(),
            )
        )