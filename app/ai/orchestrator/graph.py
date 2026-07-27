"""
Enterprise AI workflow using LangGraph.
"""

from __future__ import annotations

import logging

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.ai.agents.models import SupervisorDecision
from app.ai.agents.registry import AgentRegistry
from app.ai.orchestrator.state import WorkflowState
from app.ai.planner.planner_service import PlannerService
from app.ai.services.supervisor_service import SupervisorService
from app.ai.workflow.models import WorkflowExecution
from app.ai.workflow.models import WorkflowStatus
from app.ai.workflow.workflow_service import WorkflowService

logger = logging.getLogger(__name__)


class WorkflowGraph:
    """
    Enterprise AI workflow orchestrated using LangGraph.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
        supervisor_service: SupervisorService,
        planner_service: PlannerService,
        workflow_service: WorkflowService,
    ) -> None:

        self._agent_registry = agent_registry
        self._supervisor_service = supervisor_service
        self._planner_service = planner_service
        self._workflow_service = workflow_service

        workflow = StateGraph(WorkflowState)

        workflow.add_node(
            "process_request",
            self._process_request,
        )

        workflow.add_edge(
            START,
            "process_request",
        )

        workflow.add_edge(
            "process_request",
            END,
        )

        self._graph = workflow.compile()

    async def _process_request(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Process a user request.
        """

        user_input = state["user_input"]

        logger.info(
            "Processing user request: %s",
            user_input,
        )

        decision = await self._supervisor_service.decide(
            user_input
        )

        logger.info(
            "Supervisor decision: agent='%s', user_input='%s', parameters=%s",
            decision.agent,
            decision.user_input,
            decision.parameters,
        )

        if decision.agent == "planner":

            state["response"] = await self._execute_workflow(
                decision,
            )

        else:

            state["response"] = await self._execute_single_agent(
                decision,
            )

        return state

    async def _execute_workflow(
        self,
        decision: SupervisorDecision,
    ) -> str:
        """
        Execute a multi-step workflow.
        """

        logger.info(
            "Supervisor selected Planner."
        )

        planner_response = await self._planner_service.create_plan(
            decision.user_input,
        )

        logger.info(
            "Planner generated %d workflow step(s).",
            len(
                planner_response.execution_plan.steps
            ),
        )

        execution = WorkflowExecution(
            execution_plan=planner_response.execution_plan,
        )

        workflow_execution = await self._workflow_service.execute(
            execution,
        )

        return self._build_workflow_response(
            workflow_execution,
        )

    async def _execute_single_agent(
        self,
        decision: SupervisorDecision,
    ) -> str:
        """
        Execute a single agent.
        """

        agent = self._agent_registry.get(
            decision.agent,
        )

        logger.info(
            "Executing agent='%s' user_input='%s' parameters=%s",
            decision.agent,
            decision.user_input,
            decision.parameters,
        )

        result = await agent.execute(
            decision.user_input,
            decision.parameters,
        )

        logger.info(
            "Agent execution completed: success=%s",
            result.success,
        )

        if result.success:
            return str(result.result)

        return str(result.error)

    def _build_workflow_response(
        self,
        workflow_execution: WorkflowExecution,
    ) -> str:
        """
        Build the final response from a workflow execution.
        """

        if workflow_execution.status != WorkflowStatus.COMPLETED:

            return (
                f"Workflow failed: "
                f"{workflow_execution.error}"
            )

        if not workflow_execution.steps:

            return "Workflow completed."

        last_step = workflow_execution.steps[-1]

        if (
            last_step.output
            and last_step.output.result is not None
        ):
            return str(last_step.output.result)

        return "Workflow completed."

    async def invoke(
        self,
        user_input: str,
    ) -> str:
        """
        Execute the LangGraph workflow.
        """

        result = await self._graph.ainvoke(
            {
                "user_input": user_input,
                "response": "",
            }
        )

        return result["response"]