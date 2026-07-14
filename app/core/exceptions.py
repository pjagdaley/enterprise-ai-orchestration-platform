"""
Custom application exceptions.
"""


class ApplicationException(Exception):
    """Base class for all application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "APPLICATION_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


class ResourceNotFoundException(ApplicationException):
    def __init__(self, resource: str):
        super().__init__(
            message=f"{resource} not found.",
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
        )


class ValidationException(ApplicationException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
        )


class UnauthorizedException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Unauthorized.",
            status_code=401,
            error_code="UNAUTHORIZED",
        )


class ForbiddenException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Access denied.",
            status_code=403,
            error_code="FORBIDDEN",
        )