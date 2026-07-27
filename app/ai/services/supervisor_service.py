"""
Supervisor Service.
"""

from __future__ import annotations

import json
import logging

from pydantic import ValidationError
from app.utils.json_utils import clean_llm_json

from app.ai.agents.models import SupervisorDecision
from app.ai.llm.factory import LLMFactory
from app.ai.llm.models import LLMRequest
from app.ai.prompts.supervisor_prompt_builder import (
    SupervisorPromptBuilder,
)
from app.core.exceptions import SupervisorException

logger = logging.getLogger(__name__)


class SupervisorService:
    """
    Uses an LLM to determine which agent should execute
    a user request.
    """

    def __init__(self) -> None:
        self._llm = LLMFactory.create()
        self._prompt_builder = SupervisorPromptBuilder()

    async def decide(
        self,
        user_input: str,
    ) -> SupervisorDecision:
        """
        Determine which agent should handle the request.

        Args:
            user_input:
                Original user request.

        Returns:
            SupervisorDecision
        """

        logger.info(
            "Generating supervisor decision for request='%s'",
            user_input,
        )

        prompt = self._prompt_builder.build_prompt(
            user_input=user_input,
        )

        response = await self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        logger.info("Supervisor response received.")

        cleaned_json = clean_llm_json(
            response.content
        )

        try:

            #
            # Validate JSON syntax.
            #
            json.loads(cleaned_json)

            #
            # Validate against domain model.
            #
            decision = (
                SupervisorDecision.model_validate_json(
                    cleaned_json
                )
            )

        except json.JSONDecodeError as ex:

            logger.exception(
                "Supervisor produced invalid JSON."
            )

            raise SupervisorException(
                "Supervisor returned invalid JSON."
            ) from ex

        except ValidationError as ex:

            logger.exception(
                "Supervisor returned an invalid decision."
            )

            raise SupervisorException(
                "Supervisor returned an invalid decision."
            ) from ex

        logger.info(
            "Supervisor selected agent='%s'.",
            decision.agent,
        )

        return decision