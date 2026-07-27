"""
Workflow service.
"""

from app.ai.agents.registry import AgentRegistry
from app.ai.workflow.context import WorkflowContext
from app.ai.workflow.executor import WorkflowExecutor
from app.ai.workflow.models import WorkflowExecution


class WorkflowService:
    """
    Workflow service.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
    ) -> None:

        self._executor = WorkflowExecutor(agent_registry)

    async def execute(
        self,
        execution: WorkflowExecution,
    ) -> WorkflowExecution:
        """
        Execute a workflow.
        """

        context = WorkflowContext()

        return await self._executor.execute(
            execution=execution,
            context=context,
        )