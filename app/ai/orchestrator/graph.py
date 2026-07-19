"""
Enterprise AI workflow using LangGraph.
"""

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.ai.agents.planner_agent import PlannerAgent
from app.ai.orchestrator.state import WorkflowState
from app.ai.tools.models import ToolRequest
from app.ai.tools.registry import ToolRegistry


class WorkflowGraph:
    """
    Enterprise AI workflow that orchestrates the execution of tools based on user input.
    """

    def __init__(self, tool_registry: ToolRegistry,) -> None:
        """
        Initialize the workflow.
        """

        self._planner = PlannerAgent()

        self._tool_registry = tool_registry
        
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

        #
        # Planner decides what to do.
        #
        decision = self._planner.plan(user_input)

        #
        # Get the selected tool.
        #
        tool = self._tool_registry.get(decision.tool)

        #
        # Execute the tool.
        #
        result = await tool.execute(
            ToolRequest(
                input=decision.input,
                parameters=decision.parameters,
            )
        )

        state["response"] = result.result

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