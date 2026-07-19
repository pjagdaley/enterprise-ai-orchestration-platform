"""
Application service for chat operations.
"""

from app.ai.orchestrator.graph import WorkflowGraph


class ChatService:
    """
    Service responsible for processing chat requests.
    """

    def __init__(self, workflow: WorkflowGraph,) -> None:
        """
        Initialize the chat service.
        """
        self._workflow = workflow

    async def chat(
        self,
        message: str,
    ) -> str:
        """
        Process a user message.

        Args:
            message:
                User input.

        Returns:
            AI generated response.
        """

        response = await self._workflow.invoke(message)

        return response