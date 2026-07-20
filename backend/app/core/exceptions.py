"""Domain and application exceptions."""

from typing import Any


class ApplicationError(Exception):
    """Base class for all application exceptions."""

    default_message: str = "An application error occurred"
    status_code: int = 500

    def __init__(self, message: str | None = None, details: dict[str, Any] | None = None):
        self.message = message or self.default_message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(ApplicationError):
    """Raised when a requested resource cannot be found."""

    default_message = "Resource not found"
    status_code = 404


class ConflictError(ApplicationError):
    """Raised when a resource conflicts with existing state."""

    default_message = "Resource conflict"
    status_code = 409


class ValidationError(ApplicationError):
    """Raised when input validation fails at the domain level."""

    default_message = "Validation failed"
    status_code = 422


class AuthenticationError(ApplicationError):
    """Raised when authentication fails."""

    default_message = "Authentication failed"
    status_code = 401


class AuthorizationError(ApplicationError):
    """Raised when a user lacks permission to perform an action."""

    default_message = "Not authorized"
    status_code = 403


class BusinessRuleViolationError(ApplicationError):
    """Raised when a business rule is violated."""

    default_message = "Business rule violation"
    status_code = 422


class ExternalServiceError(ApplicationError):
    """Raised when an external service call fails."""

    default_message = "External service error"
    status_code = 502