"""
Google Gemini implementation.
"""

from google.genai.types import GenerateContentConfig

from app.ai.llm.base_llm import BaseLLM
from app.ai.llm.exceptions import (
    LLMConnectionException,
    LLMResponseException,
)
from app.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)
from app.core.config import settings
from app.infrastructure.vertexai.client import VertexAIClient


class GeminiLLM(BaseLLM):
    """
    Google Gemini implementation.
    """

    def __init__(
        self,
        client: VertexAIClient | None = None,
    ) -> None:
        """
        Initialize the Gemini LLM.

        Args:
            client:
                Optional Vertex AI client. If not provided,
                a default client is created.
        """

        self._vertex_client = client or VertexAIClient()
        self._client = self._vertex_client.client
        self._model = settings.gemini_model

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate text using Gemini.
        """

        try:

            response = self._client.models.generate_content(
                model=self._model,
                contents=request.prompt,
                config=GenerateContentConfig(
                    temperature=request.temperature,
                    max_output_tokens=request.max_tokens,
                    top_p=request.top_p,
                ),
            )

            if not response.text:
                raise LLMResponseException(
                    "Gemini returned an empty response."
                )

            usage = getattr(response, "usage_metadata", None)

            return LLMResponse(
                content=response.text,
                model=self._model,
                finish_reason="STOP",
                prompt_tokens=getattr(
                    usage,
                    "prompt_token_count",
                    0,
                ),
                completion_tokens=getattr(
                    usage,
                    "candidates_token_count",
                    0,
                ),
                total_tokens=getattr(
                    usage,
                    "total_token_count",
                    0,
                ),
            )

        except LLMResponseException:
            raise

        except Exception as ex:
            raise LLMConnectionException(
                f"Failed to communicate with Gemini: {ex}"
            ) from ex

    async def health_check(self) -> bool:
        """
        Verify Gemini connectivity.
        """

        try:
            self._client.models.generate_content(
                model=self._model,
                contents="health check",
            )
            return True

        except Exception:
            return False