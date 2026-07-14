"""
Vertex AI client.

Provides a singleton Google GenAI client for the application.
"""

from google import genai

from app.core.config import settings


class VertexAIClient:
    """
    Wrapper around the Google GenAI client.
    """

    def __init__(self) -> None:

        self._client = genai.Client(
            vertexai=True,
            project=settings.project_id,
            location=settings.vertex_ai_location,
        )

    @property
    def client(self) -> genai.Client:
        """
        Return the underlying Google GenAI client.
        """
        return self._client