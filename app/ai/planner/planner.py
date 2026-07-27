"""
Planner implementation.
"""

from __future__ import annotations

import json
import logging

from pydantic import ValidationError

from app.ai.llm.factory import LLMFactory
from app.ai.llm.models import LLMRequest

from app.utils.json_utils import clean_llm_json

from app.ai.planner.models import PlannerResponse
from app.core.exceptions import PlannerException

from .planner_prompt import PLANNER_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class Planner:
    """
    Generates workflow execution plans using an LLM.
    """

    def __init__(self) -> None:
        self._llm = LLMFactory.create()

    async def plan(
        self,
        user_request: str,
    ) -> PlannerResponse:
        """
        Generate a validated execution plan.

        Args:
            user_request:
                Original user request.

        Returns:
            PlannerResponse
        """

        logger.info(
            "Generating execution plan for request='%s'",
            user_request,
        )

        prompt = self._build_prompt(user_request)

        response = await self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        logger.info("Planner response received.")

        cleaned_json = clean_llm_json(response.content)

        try:

            #
            # Validate JSON syntax.
            #
            json.loads(cleaned_json)

            #
            # Validate against the PlannerResponse model.
            #
            planner_response = PlannerResponse.model_validate_json(
                cleaned_json
            )

        except json.JSONDecodeError as ex:

            logger.exception(
                "Planner produced invalid JSON."
            )

            raise PlannerException(
                "Planner returned invalid JSON."
            ) from ex

        except ValidationError as ex:

            logger.exception(
                "Planner returned an invalid execution plan."
            )

            raise PlannerException(
                "Planner returned an invalid execution plan."
            ) from ex

        logger.info(
            "Execution plan generated successfully "
            "(plan_type=%s, steps=%d).",
            planner_response.plan_type.value,
            len(planner_response.execution_plan.steps),
        )

        return planner_response

    def _build_prompt(
        self,
        user_request: str,
    ) -> str:
        """
        Build the planner prompt.
        """

        return f"""{PLANNER_SYSTEM_PROMPT}

------------------------------------------------------------

User Request:

{user_request}
"""