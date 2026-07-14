"""
LLM-specific exceptions.
"""


class LLMException(Exception):
    """
    Base exception for all LLM-related errors.
    """

    pass


class LLMConnectionException(LLMException):
    """
    Raised when the LLM provider cannot be reached.
    """

    pass


class LLMAuthenticationException(LLMException):
    """
    Raised when authentication with the LLM provider fails.
    """

    pass


class LLMRateLimitException(LLMException):
    """
    Raised when the LLM provider rate limit is exceeded.
    """

    pass


class LLMTimeoutException(LLMException):
    """
    Raised when an LLM request times out.
    """

    pass


class LLMResponseException(LLMException):
    """
    Raised when an invalid response is returned by the provider.
    """

    pass