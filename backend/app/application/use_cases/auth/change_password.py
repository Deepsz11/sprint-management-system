"""Change password use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.use_cases.base import UseCase
from app.core.exceptions import AuthenticationError, NotFoundError
from app.core.security import hash_password, verify_password
from app.domain.services.password_policy import DEFAULT_PASSWORD_POLICY, PasswordPolicy


@dataclass(frozen=True)
class ChangePasswordCommand:
    """Change password command."""

    user_id: UUID
    current_password: str
    new_password: str


class ChangePasswordUseCase(UseCase[ChangePasswordCommand, None]):
    """Change a user's password after verifying their current one."""

    def __init__(self, policy: PasswordPolicy = DEFAULT_PASSWORD_POLICY) -> None:
        super().__init__()
        self._policy = policy

    def execute(self, command: ChangePasswordCommand) -> None:
        self._policy.validate(command.new_password)

        with self._uow_factory() as uow:
            user = uow.users.get_by_id(command.user_id)
            if user is None:
                raise NotFoundError(f"User {command.user_id} not found")
            if not verify_password(command.current_password, user.hashed_password):
                raise AuthenticationError("Current password is incorrect")
            if verify_password(command.new_password, user.hashed_password):
                raise AuthenticationError(
                    "New password must be different from the current password"
                )

            user.hashed_password = hash_password(command.new_password)
            user.touch()
            uow.users.update(user)
            uow.user_sessions.revoke_all_for_user(command.user_id)
            uow.commit()