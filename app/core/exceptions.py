"""
Custom application exceptions.
"""


class ApplicationException(Exception):
    """
    Base class for all application exceptions.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "APPLICATION_ERROR",
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


# ============================================================================
# General Application Exceptions
# ============================================================================


class ResourceNotFoundException(ApplicationException):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(self, resource: str) -> None:
        super().__init__(
            message=f"{resource} not found.",
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
        )


class ValidationException(ApplicationException):
    """
    Raised when validation fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
        )


class UnauthorizedException(ApplicationException):
    """
    Raised when authentication is required.
    """

    def __init__(self) -> None:
        super().__init__(
            message="Unauthorized.",
            status_code=401,
            error_code="UNAUTHORIZED",
        )


class ForbiddenException(ApplicationException):
    """
    Raised when access is denied.
    """

    def __init__(self) -> None:
        super().__init__(
            message="Access denied.",
            status_code=403,
            error_code="FORBIDDEN",
        )


# ============================================================================
# AI Platform Exceptions
# ============================================================================


class SupervisorException(ApplicationException):
    """
    Raised when the Supervisor cannot route a request.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="SUPERVISOR_ERROR",
        )


class PlannerException(ApplicationException):
    """
    Raised when the Planner cannot generate a valid execution plan.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="PLANNER_ERROR",
        )


class WorkflowException(ApplicationException):
    """
    Raised when workflow execution fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="WORKFLOW_ERROR",
        )


class AgentException(ApplicationException):
    """
    Raised when an agent execution fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="AGENT_ERROR",
        )


class ToolException(ApplicationException):
    """
    Raised when a tool execution fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="TOOL_ERROR",
        )


class MCPException(ApplicationException):
    """
    Raised when communication with an MCP server fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="MCP_ERROR",
        )


class RAGException(ApplicationException):
    """
    Raised when RAG processing fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="RAG_ERROR",
        )


class EmbeddingException(ApplicationException):
    """
    Raised when embedding generation fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="EMBEDDING_ERROR",
        )


class VectorStoreException(ApplicationException):
    """
    Raised when vector store operations fail.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="VECTOR_STORE_ERROR",
        )


class LLMException(ApplicationException):
    """
    Raised when an LLM request fails.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code="LLM_ERROR",
        )