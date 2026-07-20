"""Optional authentication middleware.

This middleware attempts to attach the current user to `request.state` when a
valid Bearer token is present. It never rejects a request on its own — route
dependencies remain the source of truth for enforcement. This design keeps
public routes (health, login, refresh, docs) unaffected while enabling
downstream code (e.g., audit logging) to access the caller when available.
"""

from __future__ import annotations

from uuid import UUID

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger
from app.core.security import decode_token
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

_logger = get_logger("api.middleware.auth")


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Attach `request.state.current_user` when a valid access token is present."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.current_user = None
        header = request.headers.get("authorization")
        if header and header.lower().startswith("bearer "):
            token = header.split(" ", 1)[1].strip()
            try:
                payload = decode_token(token)
                if payload.get("type") == "access":
                    subject = payload.get("sub")
                    if subject:
                        try:
                            user_id = UUID(subject)
                        except ValueError:
                            user_id = None
                        if user_id is not None:
                            with SQLAlchemyUnitOfWork() as uow:
                                user = uow.users.get_by_id(user_id)
                            if user is not None and user.is_active:
                                request.state.current_user = user
            except Exception as exc:  # noqa: BLE001 - defensive; enforcement happens later
                _logger.debug("Ignoring invalid Authorization header: %s", exc)

        return await call_next(request)