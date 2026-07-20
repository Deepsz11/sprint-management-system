"""Notification entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import Entity
from app.domain.enums import NotificationChannel, NotificationStatus


@dataclass
class Notification(Entity):
    """A notification delivered to a user."""

    recipient_id: UUID = field(default_factory=lambda: UUID(int=0))
    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    title: str = ""
    body: str = ""
    channel: NotificationChannel = NotificationChannel.IN_APP
    status: NotificationStatus = NotificationStatus.PENDING
    event_type: str = "generic"
    subject_type: str | None = None
    subject_id: UUID | None = None
    action_url: str | None = None
    sent_at: datetime | None = None
    read_at: datetime | None = None
    error_message: str | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Notification title is required")
        if not self.body or not self.body.strip():
            raise ValidationError("Notification body is required")

    def mark_sent(self) -> None:
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.now(timezone.utc)
        self.touch()

    def mark_read(self) -> None:
        if self.status not in {NotificationStatus.SENT, NotificationStatus.PENDING}:
            return
        self.status = NotificationStatus.READ
        self.read_at = datetime.now(timezone.utc)
        self.touch()

    def mark_failed(self, error: str) -> None:
        self.status = NotificationStatus.FAILED
        self.error_message = error
        self.touch()