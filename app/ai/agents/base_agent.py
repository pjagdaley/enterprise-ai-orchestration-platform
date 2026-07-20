"""
Base class for all AI agents.
"""

from abc import ABC
from abc import abstractmethod

from typing import Any

from app.ai.tools.models import ToolResponse


class BaseAgent(ABC):
    """
    Base class for all agents.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Agent name.
        """

    @abstractmethod
    async def execute(
        self,
        user_input: str,
        parameters: dict[str, Any],
    ) -> ToolResponse:
        """
        Execute the agent.
        """