"""Notification DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import NotificationChannel, NotificationStatus


class NotificationCreateDTO(BaseModel):
    """Payload for creating a notification."""

    recipient_id: UUID
    title: str = Field(min_length=1, max_length=300)
    body: str = Field(min_length=1, max_length=4000)
    channel: NotificationChannel = NotificationChannel.IN_APP
    event_type: str = Field(default="generic", max_length=64)
    subject_type: str | None = Field(default=None, max_length=64)
    subject_id: UUID | None = None
    action_url: str | None = Field(default=None, max_length=2000)


class NotificationDTO(BaseModel):
    """Notification response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    recipient_id: UUID
    organization_id: UUID
    title: str
    body: str
    channel: NotificationChannel
    status: NotificationStatus
    event_type: str
    subject_type: str | None
    subject_id: UUID | None
    action_url: str | None
    sent_at: datetime | None
    read_at: datetime | None
    created_at: datetime