"""
Enterprise AI workflow using LangGraph.
"""

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.ai.agents.planner_agent import PlannerAgent
from app.ai.llm.factory import LLMFactory
from app.ai.llm.models import LLMRequest
from app.ai.orchestrator.state import WorkflowState
from app.ai.tools.models import ToolRequest
from app.ai.tools.registry import ToolRegistry


class WorkflowGraph:
    """
    Enterprise AI workflow.
    """

    def __init__(self) -> None:
        """
        Initialize the workflow.
        """

        self._planner = PlannerAgent()

        self._llm = LLMFactory.create()

        self._tool_registry = ToolRegistry()
        self._tool_registry.register_all()

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
        # Planner decides what to do
        #
        decision = self._planner.plan(user_input)

        tool = self._tool_registry.get(decision)

        result = await tool.execute(
            ToolRequest(
                input=user_input,
            )
        )

        state["response"] = result.result

        return state
    """   
        #
        # Calculator Tool
        #
        if decision == "calculator":

            calculator = self._tool_registry.get("calculator")

            result = await calculator.execute(
                ToolRequest(
                    input=user_input,
                )
            )

            state["response"] = result.result

            return state

        #
        # Default -> LLM
        #
        response = await self._llm.generate(
            LLMRequest(
                prompt=user_input,
            )
        )

        state["response"] = response.content

        return state
    """    

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