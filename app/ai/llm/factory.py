"""
Factory for creating LLM provider instances.
"""

from typing import Type

from app.ai.llm.base_llm import BaseLLM
from app.ai.llm.exceptions import LLMException
from app.ai.llm.gemini_llm import GeminiLLM
from app.ai.llm.mock_llm import MockLLM
from app.core.config import settings


class LLMFactory:
    """
    Factory responsible for creating LLM provider instances.
    """

    _providers: dict[str, Type[BaseLLM]] = {
        "mock": MockLLM,
        "gemini": GeminiLLM,
    }

    @classmethod
    def create(cls) -> BaseLLM:
        """
        Create an LLM provider based on application configuration.

        Returns:
            BaseLLM implementation.

        Raises:
            LLMException:
                If the configured provider is not supported.
        """

        provider = settings.llm_provider.lower()

        provider_class = cls._providers.get(provider)

        if provider_class is None:
            supported = ", ".join(sorted(cls._providers.keys()))

            raise LLMException(
                f"Unsupported LLM provider: '{provider}'. "
                f"Supported providers: {supported}"
            )

        return provider_class()

    @classmethod
    def register(
        cls,
        name: str,
        provider: Type[BaseLLM],
    ) -> None:
        """
        Register a new LLM provider.

        Args:
            name:
                Provider name.

            provider:
                Provider implementation.
        """

        cls._providers[name.lower()] = provider

    @classmethod
    def supported_providers(cls) -> list[str]:
        """
        Return the list of supported providers.
        """

        return sorted(cls._providers.keys())