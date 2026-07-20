"""Logout use cases."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.use_cases.base import UseCase
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.infrastructure.security.token_hasher import hash_token


@dataclass(frozen=True)
class LogoutCommand:
    """Logout a single session identified by its refresh token."""

    refresh_token: str


class LogoutUseCase(UseCase[LogoutCommand, None]):
    """Revoke the session tied to a refresh token."""

    def execute(self, command: LogoutCommand) -> None:
        payload = decode_token(command.refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Provided token is not a refresh token")

        token_hash = hash_token(command.refresh_token)
        with self._uow_factory() as uow:
            session = uow.user_sessions.get_by_token_hash(token_hash)
            if session is not None and session.is_active:
                session.revoke()
                uow.user_sessions.update(session)
                uow.commit()


@dataclass(frozen=True)
class LogoutAllCommand:
    """Revoke every active session for a user."""

    user_id: UUID


class LogoutAllUseCase(UseCase[LogoutAllCommand, int]):
    """Revoke every active session for a given user."""

    def execute(self, command: LogoutAllCommand) -> int:
        with self._uow_factory() as uow:
            count = uow.user_sessions.revoke_all_for_user(command.user_id)
            uow.commit()
            return count