"""API-layer security dependencies for authentication and authorization."""

from __future__ import annotations

from typing import Annotated, Callable
from uuid import UUID

from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer

from app.application.context import RequestContext
from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token
from app.domain.entities.user import User
from app.domain.enums import UserRole
from app.domain.services.permissions import Permission, PermissionRegistry
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False,
)


def _extract_bearer(request: Request, token: str | None) -> str:
    if token:
        return token
    header = request.headers.get("authorization")
    if header and header.lower().startswith("bearer "):
        return header.split(" ", 1)[1].strip()
    raise AuthenticationError("Authentication credentials were not provided")


def get_authenticated_user(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
) -> User:
    """Resolve the currently authenticated user from a Bearer access token."""
    raw = _extract_bearer(request, token)
    payload = decode_token(raw)
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

    request.state.current_user = user
    return user


def build_request_context(
    request: Request,
    user: Annotated[User, Depends(get_authenticated_user)],
    x_forwarded_for: Annotated[str | None, Header(alias="X-Forwarded-For")] = None,
) -> RequestContext:
    """Build a RequestContext for downstream use cases."""
    ip_address = x_forwarded_for or (request.client.host if request.client else None)
    user_agent = request.headers.get("user-agent")
    return RequestContext(actor=user, ip_address=ip_address, user_agent=user_agent)


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    """Dependency factory: require the current user to hold one of the given roles."""

    def _dep(user: Annotated[User, Depends(get_authenticated_user)]) -> User:
        if user.role not in roles:
            allowed = ", ".join(r.value for r in roles)
            raise AuthorizationError(f"This action requires one of: {allowed}")
        return user

    return _dep


def require_permissions(*permissions: Permission) -> Callable[[User], User]:
    """Dependency factory: require the caller to have every listed permission."""

    def _dep(user: Annotated[User, Depends(get_authenticated_user)]) -> User:
        for permission in permissions:
            PermissionRegistry.ensure(user, permission)
        return user

    return _dep


def require_any_permission(*permissions: Permission) -> Callable[[User], User]:
    """Dependency factory: require the caller to have at least one listed permission."""

    def _dep(user: Annotated[User, Depends(get_authenticated_user)]) -> User:
        PermissionRegistry.ensure_any(user, *permissions)
        return user

    return _dep