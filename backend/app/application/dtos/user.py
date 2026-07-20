"""User DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.enums import UserRole, UserStatus


class UserCreateDTO(BaseModel):
    """Payload for creating a user (self-registration or admin create)."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)
    organization_id: UUID | None = None
    role: UserRole = UserRole.VIEWER


class UserInviteDTO(BaseModel):
    """Payload for inviting a user to an organization."""

    email: EmailStr
    full_name: str = Field(min_length=1, max_length=200)
    role: UserRole = UserRole.VIEWER


class UserUpdateDTO(BaseModel):
    """Payload for updating a user."""

    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    role: UserRole | None = None
    status: UserStatus | None = None


class UserDTO(BaseModel):
    """User response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: str
    organization_id: UUID | None
    role: UserRole
    status: UserStatus
    last_login_at: datetime | None
    is_email_verified: bool
    created_at: datetime
    updated_at: datetime