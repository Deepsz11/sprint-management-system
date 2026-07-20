"""Refresh access token use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.auth import TokenDTO
from app.application.use_cases.base import UseCase
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.domain.enums import UserStatus


@dataclass(frozen=True)
class RefreshTokenCommand:
    """Refresh token command payload."""

    refresh_token: str


class RefreshTokenUseCase(UseCase[RefreshTokenCommand, TokenDTO]):
    """Issue a new access token given a valid refresh token."""

    def execute(self, command: RefreshTokenCommand) -> TokenDTO:
        payload = decode_token(command.refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Provided token is not a refresh token")

        subject = payload.get("sub")
        if not subject:
            raise AuthenticationError("Refresh token missing subject")

        try:
            user_id = UUID(subject)
        except ValueError as exc:
            raise AuthenticationError("Invalid subject in token") from exc

        with self._uow_factory() as uow:
            user = uow.users.get_by_id(user_id)
            if user is None or user.status != UserStatus.ACTIVE:
                raise AuthenticationError("User is not active")

            access_token = create_access_token(
                subject=user.id,
                additional_claims={
                    "role": user.role.value,
                    "org": str(user.organization_id) if user.organization_id else None,
                },
            )
            refresh_token = create_refresh_token(subject=user.id)

            return TokenDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )