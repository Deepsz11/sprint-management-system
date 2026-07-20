"""FastAPI dependency providers."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer

from app.application.context import RequestContext
from app.application.services.audit_service import AuditService
from app.application.services.notification_service import NotificationService
from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token
from app.domain.entities.user import User
from app.domain.enums import UserRole
from app.domain.services.authorization_service import AuthorizationDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False,
)


def get_uow_factory() -> type[SQLAlchemyUnitOfWork]:
    """Return the concrete Unit-of-Work factory type."""
    return SQLAlchemyUnitOfWork


def get_uow() -> SQLAlchemyUnitOfWork:
    """Return an unopened Unit-of-Work instance. Callers must use it as a ctx manager."""
    return SQLAlchemyUnitOfWork()


def get_current_user(
    request: Request,
    token: Annotated[str | None, Depends(_oauth2_scheme)],
) -> User:
    """Resolve the current authenticated user from a Bearer token."""
    if not token:
        raise AuthenticationError("Authentication credentials were not provided")

    payload = decode_token(token)
    if payload.get("type") != "access":
        raise AuthenticationError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise AuthenticationError("Token missing subject")

    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise AuthenticationError("Invalid subject in token") from exc

    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise AuthenticationError("User not found")
        if not user.is_active:
            raise AuthenticationError("User account is not active")

    # Cache on request for downstream services
    request.state.current_user = user
    return user


def get_request_context(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    x_forwarded_for: Annotated[str | None, Header(alias="X-Forwarded-For")] = None,
) -> RequestContext:
    """Build a RequestContext for use cases."""
    ip_address = x_forwarded_for or (request.client.host if request.client else None)
    user_agent = request.headers.get("user-agent")
    return RequestContext(
        actor=current_user,
        ip_address=ip_address,
        user_agent=user_agent,
    )


def require_roles(*roles: UserRole):
    """Return a dependency that requires the current user to have one of the given roles."""

    def _dependency(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in roles:
            raise AuthorizationError(
                f"This action requires one of roles: {', '.join(r.value for r in roles)}"
            )
        return user

    return _dependency


def require_admin(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require an admin-level user."""
    if not AuthorizationDomainService.can_manage_organization(user):
        raise AuthorizationError("Administrator privileges required")
    return user


def get_audit_service(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_uow)],
) -> AuditService:
    """Return an AuditService bound to a fresh session."""
    uow.__enter__()
    try:
        return AuditService(uow.audit_logs)
    finally:
        # Session lifetime is managed by the caller via context manager; we
        # deliberately do not close here as the same session is reused.
        pass


def get_notification_service(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_uow)],
) -> NotificationService:
    """Return a NotificationService bound to a fresh session."""
    uow.__enter__()
    return NotificationService(uow.notifications)