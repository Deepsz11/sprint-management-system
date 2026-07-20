"""Extended authentication DTOs (password change, session listing, logout)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LogoutDTO(BaseModel):
    """Payload for logging out a specific session."""

    refresh_token: str = Field(min_length=1)


class LogoutAllDTO(BaseModel):
    """Empty payload marker for logging out of all sessions."""

    model_config = ConfigDict(frozen=True)


class ChangePasswordDTO(BaseModel):
    """Payload for changing the current user's password."""

    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UserSessionDTO(BaseModel):
    """User session response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    issued_at: datetime
    expires_at: datetime
    revoked_at: datetime | None
    ip_address: str | None
    user_agent: str | None
    last_used_at: datetime | None
    created_at: datetime