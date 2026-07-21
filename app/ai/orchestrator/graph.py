"""
Enterprise AI workflow using LangGraph.
"""

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.ai.agents.supervisor_agent import SupervisorAgent
from app.ai.orchestrator.state import WorkflowState
from app.ai.agents.registry import AgentRegistry

import logging

logger = logging.getLogger(__name__)

class WorkflowGraph:
    """
    Enterprise AI workflow that orchestrates the execution of tools based on user input.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
    ) -> None:
        """
        Initialize the workflow.
        """

        self._supervisor = SupervisorAgent()

        self._agent_registry = agent_registry

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
        Process the user request.
        """

        user_input = state["user_input"]
        logger.info("Processing user request: %s", user_input)

        #
        # Supervisor decides what to do.
        #
        decision = self._supervisor.decide(user_input)
        logger.info(
            "Supervisor decision: agent='%s', input='%s', parameters=%s",
            decision.agent,
            decision.input,
            decision.parameters,
        )

        #
        # Get the selected agent.
        #
        agent = self._agent_registry.get(decision.agent)
        
        #
        # Execute the agent.
        #
        logger.info(
            "Executing agent='%s' with input='%s' and parameters=%s",
            decision.agent,
            decision.input,
            decision.parameters
        )
        result = await agent.execute(
            decision.input,
            decision.parameters,
        )

        state["response"] = result.result
        logger.info(
            "Agent returned ToolResponse: success=%s result=%r error=%r",
            result.success,
            result.result,
            result.error,
        )

        return state

    async def invoke(
        self,
        user_input: str,
    ) -> str:
        """
        Execute the workflow.
        """

        result = await self._graph.ainvoke(
            {
                "user_input": user_input,
                "response": "",
            }
        )

        return result["response"]