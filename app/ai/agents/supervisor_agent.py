"""
Supervisor Agent.

Determines how a user request should be processed.
"""

import logging
import re
from app.ai.agents.models import SupervisorDecision
from app.ai.services.supervisor_service import SupervisorService

logger = logging.getLogger(__name__)


class SupervisorAgent:

    def __init__(self):

        self._service = SupervisorService()

      
    async def decide(
        self,
        user_input: str,        
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