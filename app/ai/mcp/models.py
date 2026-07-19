"""
MCP domain models.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class MCPTool:
    """
    Represents a tool exposed by an MCP server.
    """

    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MCPToolCall:
    """
    Request to invoke an MCP tool.
    """

    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MCPResponse:
    """
    Normalized response returned from an MCP tool.
    """

    success: bool

    # Primary payload returned by the tool.
    # Can be a string, list, dict, etc.
    data: Any = None

    # Error message if the tool execution failed.
    error: str | None = None