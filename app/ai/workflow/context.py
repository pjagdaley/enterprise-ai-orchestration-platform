"""
Workflow execution context.
"""

from __future__ import annotations

from typing import Any


class WorkflowContext:
    """
    Shared context for a single workflow execution.

    Stores intermediate results that can be consumed
    by subsequent workflow steps.
    """

    def __init__(self) -> None:
        """
        Initialize an empty workflow context.
        """

        self._variables: dict[str, Any] = {}

        self._current_step: int = 0

    @property
    def current_step(self) -> int:
        """
        Return the current workflow step.
        """

        return self._current_step

    @current_step.setter
    def current_step(
        self,
        step: int,
    ) -> None:
        """
        Update the current workflow step.
        """

        self._current_step = step

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a value in the workflow context.
        """

        self._variables[key] = value

    def get(
        self,
        key: str,
        default: Any | None = None,
    ) -> Any:
        """
        Retrieve a value from the workflow context.
        """

        return self._variables.get(key, default)

    def contains(
        self,
        key: str,
    ) -> bool:
        """
        Check whether a variable exists.
        """

        return key in self._variables

    def remove(
        self,
        key: str,
    ) -> None:
        """
        Remove a variable.
        """

        self._variables.pop(key, None)

    def clear(self) -> None:
        """
        Clear the workflow context.
        """

        self._variables.clear()

        self._current_step = 0

    def as_dict(self) -> dict[str, Any]:
        """
        Return the workflow context as a dictionary.
        """

        return dict(self._variables)