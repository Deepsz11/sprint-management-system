"""Notification application service."""

from __future__ import annotations

from uuid import UUID

from app.domain.entities.notification import Notification
from app.domain.enums import NotificationChannel, NotificationStatus
from app.domain.repositories.notification_repository import (
    NotificationRepositoryContract,
)


class NotificationService:
    """Creates and dispatches user-facing notifications."""

    def __init__(self, repository: NotificationRepositoryContract) -> None:
        self._repository = repository

    def notify(
        self,
        *,
        recipient_id: UUID,
        organization_id: UUID,
        title: str,
        body: str,
        event_type: str,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        subject_type: str | None = None,
        subject_id: UUID | None = None,
        action_url: str | None = None,
    ) -> Notification:
        """Create a pending notification for a recipient."""
        notification = Notification(
            recipient_id=recipient_id,
            organization_id=organization_id,
            title=title,
            body=body,
            channel=channel,
            status=NotificationStatus.PENDING,
            event_type=event_type,
            subject_type=subject_type,
            subject_id=subject_id,
            action_url=action_url,
        )
        return self._repository.add(notification)

    def mark_read(self, notification_id: UUID) -> Notification:
        """Mark a notification as read."""
        notification = self._repository.get_by_id(notification_id)
        if notification is None:
            raise ValueError(f"Notification {notification_id} not found")
        notification.mark_read()
        return self._repository.update(notification)

    def mark_all_read(self, recipient_id: UUID) -> int:
        """Mark all pending/sent notifications for a recipient as read."""
        return self._repository.mark_all_read(recipient_id)