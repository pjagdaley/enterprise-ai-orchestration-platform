"""
State definition for the LangGraph workflow.
"""

from typing import TypedDict


class WorkflowState(TypedDict):
    """
    Shared state passed between LangGraph nodes.
    """

    user_input: str
    response: str