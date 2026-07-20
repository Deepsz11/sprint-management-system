"""User session entity for refresh-token lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import Entity


@dataclass
class UserSession(Entity):
    """A persistent user session backing a refresh token."""

    user_id: UUID = field(default_factory=lambda: UUID(int=0))
    refresh_token_hash: str = ""
    issued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    revoked_at: datetime | None = None
    replaced_by_session_id: UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    last_used_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.refresh_token_hash:
            raise ValidationError("refresh_token_hash is required")
        if self.expires_at <= self.issued_at:
            raise ValidationError("Session expires_at must be after issued_at")

    @property
    def is_active(self) -> bool:
        now = datetime.now(timezone.utc)
        return self.revoked_at is None and self.expires_at > now

    def revoke(self, replaced_by: UUID | None = None) -> None:
        if self.revoked_at is None:
            self.revoked_at = datetime.now(timezone.utc)
            self.replaced_by_session_id = replaced_by
            self.touch()

    def record_use(self) -> None:
        self.last_used_at = datetime.now(timezone.utc)
        self.touch()