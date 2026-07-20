"""User self-registration use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.user import UserDTO
from app.application.mappers import user_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import ConflictError
from app.core.security import hash_password
from app.domain.entities.user import User
from app.domain.enums import UserRole, UserStatus
from app.domain.value_objects import Email


@dataclass(frozen=True)
class RegisterCommand:
    """Register command payload."""

    email: str
    password: str
    full_name: str
    organization_id: UUID | None = None
    role: UserRole = UserRole.VIEWER


class RegisterUseCase(UseCase[RegisterCommand, UserDTO]):
    """Register a new user account."""

    def execute(self, command: RegisterCommand) -> UserDTO:
        with self._uow_factory() as uow:
            if uow.users.email_exists(command.email):
                raise ConflictError(f"Email {command.email} is already registered")

            user = User(
                email=Email(command.email),
                hashed_password=hash_password(command.password),
                full_name=command.full_name,
                organization_id=command.organization_id,
                role=command.role,
                status=UserStatus.ACTIVE,
                is_email_verified=False,
            )
            created = uow.users.add(user)
            uow.commit()
            return user_to_dto(created)