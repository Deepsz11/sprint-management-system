"""User aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import UserRole, UserStatus
from app.domain.value_objects import Email


@dataclass
class User(SoftDeletableEntity):
    """A user of the system."""

    email: Email = field(default_factory=lambda: Email("user@example.com"))
    hashed_password: str = ""
    full_name: str = ""
    organization_id: UUID | None = None
    role: UserRole = UserRole.VIEWER
    status: UserStatus = UserStatus.INVITED
    last_login_at: datetime | None = None
    is_email_verified: bool = False

    def __post_init__(self) -> None:
        if not self.full_name or not self.full_name.strip():
            raise ValidationError("Full name is required")
        if len(self.full_name) > 200:
            raise ValidationError("Full name must be 200 characters or fewer")

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE and not self.is_deleted

    def activate(self) -> None:
        self.status = UserStatus.ACTIVE
        self.touch()

    def suspend(self) -> None:
        self.status = UserStatus.SUSPENDED
        self.touch()

    def deactivate(self) -> None:
        self.status = UserStatus.DEACTIVATED
        self.touch()

    def record_login(self, when: datetime) -> None:
        self.last_login_at = when
        self.touch()

    def change_role(self, new_role: UserRole) -> None:
        self.role = new_role
        self.touch()

    def verify_email(self) -> None:
        self.is_email_verified = True
        self.touch()

    def has_role(self, *roles: UserRole) -> bool:
        return self.role in roles


@dataclass
class TeamMembership(SoftDeletableEntity):
    """Association between a user and a team."""

    team_id: UUID = field(default_factory=lambda: UUID(int=0))
    user_id: UUID = field(default_factory=lambda: UUID(int=0))
    is_lead: bool = False