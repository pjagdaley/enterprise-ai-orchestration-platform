"""
LangGraph workflow.
"""

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.ai.llm.factory import LLMFactory
from app.ai.llm.models import LLMRequest
from app.ai.orchestrator.state import WorkflowState


class WorkflowGraph:
    """
    Enterprise AI workflow.
    """

    def __init__(self):

        self._llm = LLMFactory.create()

        workflow = StateGraph(WorkflowState)

        workflow.add_node(
            "llm",
            self._invoke_llm,
        )

        workflow.add_edge(
            START,
            "llm",
        )

        workflow.add_edge(
            "llm",
            END,
        )

        self._graph = workflow.compile()

    async def _invoke_llm(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Invoke the configured LLM.
        """

        request = LLMRequest(
            prompt=state["user_input"],
        )

        response = await self._llm.generate(request)

        state["response"] = response.content

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