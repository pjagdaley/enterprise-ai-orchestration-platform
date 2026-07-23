"""
Supervisor Service.
"""

from __future__ import annotations

import json
import logging

from app.ai.llm.factory import LLMFactory
from app.ai.llm.models import LLMRequest
from app.ai.agents.models import SupervisorDecision
from app.ai.prompts.supervisor_prompt_builder import SupervisorPromptBuilder

logger = logging.getLogger(__name__)


class SupervisorService:
    """
    Uses an LLM to determine which agent should execute a user request.
    """

    def __init__(self) -> None:

        self._llm = LLMFactory.create()

        self._prompt_builder = SupervisorPromptBuilder()

    async def execute(
        self,
        user_input: str,
    ) -> SupervisorDecision:
        """
        Determine which agent should handle the request.
        """

        #
        # Build Prompt
        #

        prompt = self._prompt_builder.build_prompt(
            user_input=user_input,
        )

        logger.info(
            "Calling Supervisor LLM..."
        )

        #
        # Call LLM
        #

        response = await self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        logger.info(
            "Supervisor LLM Response: %s",
            response.content,
        )

        #
        # Parse JSON
        #

        content = (
            response.content.strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        decision = SupervisorDecision.model_validate(
            json.loads(content)
        )       

        logger.info(
            "Supervisor Decision: %s",
            decision,
        )

        return decision