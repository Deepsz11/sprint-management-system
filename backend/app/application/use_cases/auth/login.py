"""Login use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.application.dtos.auth import TokenDTO
from app.application.use_cases.base import UseCase
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.domain.enums import UserStatus


@dataclass(frozen=True)
class LoginCommand:
    """Login command payload."""

    email: str
    password: str
    ip_address: str | None = None
    user_agent: str | None = None


class LoginUseCase(UseCase[LoginCommand, TokenDTO]):
    """Authenticate a user and return an access/refresh token pair."""

    def execute(self, command: LoginCommand) -> TokenDTO:
        with self._uow_factory() as uow:
            user = uow.users.get_by_email(command.email)
            if user is None:
                raise AuthenticationError("Invalid email or password")
            if not verify_password(command.password, user.hashed_password):
                raise AuthenticationError("Invalid email or password")
            if user.status != UserStatus.ACTIVE:
                raise AuthenticationError(
                    f"Account is not active (status: {user.status.value})"
                )

            user.record_login(datetime.now(timezone.utc))
            uow.users.update(user)
            uow.commit()

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