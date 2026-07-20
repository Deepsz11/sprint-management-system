"""Application service that coordinates authentication flows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.domain.entities.session import UserSession
from app.domain.entities.user import User
from app.domain.enums import UserStatus
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork
from app.infrastructure.security.token_hasher import hash_token


@dataclass(frozen=True)
class AuthenticationResult:
    """Result of a successful authentication."""

    user: User
    access_token: str
    refresh_token: str
    expires_in: int


class AuthenticationService:
    """Orchestrates login, refresh, and session persistence."""

    def __init__(
        self, uow_factory: type[SQLAlchemyUnitOfWork] = SQLAlchemyUnitOfWork
    ) -> None:
        self._uow_factory = uow_factory

    def _issue(
        self,
        user: User,
        ip_address: str | None,
        user_agent: str | None,
        previous_session_id: UUID | None = None,
    ) -> AuthenticationResult:
        access_token = create_access_token(
            subject=user.id,
            additional_claims={
                "role": user.role.value,
                "org": str(user.organization_id) if user.organization_id else None,
            },
        )
        refresh_token = create_refresh_token(subject=user.id)
        now = datetime.now(timezone.utc)
        session = UserSession(
            user_id=user.id,
            refresh_token_hash=hash_token(refresh_token),
            issued_at=now,
            expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        with self._uow_factory() as uow:
            uow.user_sessions.add(session)
            if previous_session_id is not None:
                prev = uow.user_sessions.get_by_id(previous_session_id)
                if prev is not None and prev.is_active:
                    prev.revoke(replaced_by=session.id)
                    uow.user_sessions.update(prev)
            user.record_login(now)
            uow.users.update(user)
            uow.commit()

        return AuthenticationResult(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def login(
        self,
        email: str,
        password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuthenticationResult:
        with self._uow_factory() as uow:
            user = uow.users.get_by_email(email)
            if user is None or not verify_password(password, user.hashed_password):
                raise AuthenticationError("Invalid email or password")
            if user.status != UserStatus.ACTIVE:
                raise AuthenticationError(
                    f"Account is not active (status: {user.status.value})"
                )
        return self._issue(user, ip_address, user_agent)

    def refresh(
        self,
        refresh_token: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuthenticationResult:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Provided token is not a refresh token")

        subject = payload.get("sub")
        if not subject:
            raise AuthenticationError("Refresh token missing subject")
        try:
            user_id = UUID(subject)
        except ValueError as exc:
            raise AuthenticationError("Invalid subject in token") from exc

        token_hash = hash_token(refresh_token)
        with self._uow_factory() as uow:
            session = uow.user_sessions.get_by_token_hash(token_hash)
            if session is None:
                raise AuthenticationError("Session not found for this refresh token")
            if not session.is_active:
                raise AuthenticationError("Refresh token has been revoked or expired")
            if session.user_id != user_id:
                raise AuthenticationError("Refresh token does not match session owner")

            user = uow.users.get_by_id(user_id)
            if user is None or user.status != UserStatus.ACTIVE:
                raise AuthenticationError("User is not active")

            session.record_use()
            uow.user_sessions.update(session)
            uow.commit()

        return self._issue(user, ip_address, user_agent, previous_session_id=session.id)

    def logout(self, refresh_token: str) -> None:
        token_hash = hash_token(refresh_token)
        with self._uow_factory() as uow:
            session = uow.user_sessions.get_by_token_hash(token_hash)
            if session is not None and session.is_active:
                session.revoke()
                uow.user_sessions.update(session)
                uow.commit()

    def logout_all(self, user_id: UUID) -> int:
        with self._uow_factory() as uow:
            count = uow.user_sessions.revoke_all_for_user(user_id)
            uow.commit()
            return count