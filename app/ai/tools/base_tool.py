"""
Abstract base class for AI tools.
"""

from abc import ABC
from abc import abstractmethod

from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse


class BaseTool(ABC):
    """
    Base interface for all AI tools.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tool name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Tool description.
        """
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute the tool.
        """
        raise NotImplementedError