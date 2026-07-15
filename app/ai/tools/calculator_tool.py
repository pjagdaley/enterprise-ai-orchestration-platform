"""
Calculator tool.

Performs basic arithmetic operations.
"""

import ast
import operator

from app.ai.tools.base_tool import BaseTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse


class CalculatorTool(BaseTool):
    """
    Tool for evaluating basic arithmetic expressions.
    """

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Performs basic arithmetic calculations."

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute the calculator tool.
        """

        try:
            result = self._evaluate(request.input)

            return ToolResponse(
                success=True,
                result=str(result),
            )

        except Exception as ex:
            return ToolResponse(
                success=False,
                result=str(ex),
            )

    def _evaluate(self, expression: str):
        """
        Safely evaluate a simple arithmetic expression.
        """

        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
        }

        def evaluate(node):
            if isinstance(node, ast.Constant):
                return node.value

            if isinstance(node, ast.Num):  # For older Python versions
                return node.n

            if isinstance(node, ast.BinOp):
                return operators[type(node.op)](
                    evaluate(node.left),
                    evaluate(node.right),
                )

            if isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](
                    evaluate(node.operand),
                )

            raise ValueError("Unsupported expression.")

        tree = ast.parse(
            expression,
            mode="eval",
        )

        return evaluate(tree.body)