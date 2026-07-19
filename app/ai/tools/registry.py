"""
Registry for AI tools.
"""

from app.ai.tools.base_tool import BaseTool
from app.ai.tools.calculator_tool import CalculatorTool
from app.ai.tools.rag_tool import RAGTool

from app.ai.mcp.service import MCPService
from app.ai.tools.mcp_tool import MCPTool


class ToolRegistry:
    """
    Stores and retrieves AI tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register a tool.
        """

        self._tools[tool.name] = tool

    def get(
        self,
        name: str,
    ) -> BaseTool:
        """
        Retrieve a tool by name.

        Raises:
            KeyError:
                If the tool is not registered.
        """

        return self._tools[name]

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a tool is registered.
        """

        return name in self._tools

    def list_tools(
        self,
    ) -> list[str]:
        """
        Return registered tool names.
        """

        return sorted(self._tools.keys())
        