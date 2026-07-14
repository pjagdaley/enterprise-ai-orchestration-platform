"""
Abstract base interface for all Large Language Models.
"""

from abc import ABC, abstractmethod
from typing import Any

from app.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)


class BaseLLM(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    async def generate(self, request: LLMRequest,) -> LLMResponse:
        """
        Generate a response from the language model.

        Args:
            prompt:
                Input prompt.

            **kwargs:
                Provider-specific parameters.

        Returns:
            Generated response.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify that the model is reachable.

        Returns:
            True if healthy.
        """
        raise NotImplementedError