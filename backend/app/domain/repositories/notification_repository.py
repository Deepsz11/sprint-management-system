"""Repository contract for the Notification aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.notification import Notification
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import NotificationFilter, PageRequest


class NotificationRepositoryContract(Repository[Notification], ABC):
    """Repository contract for the Notification aggregate."""

    @abstractmethod
    def list_by_recipient(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        """Return notifications for a recipient ordered newest-first."""

    @abstractmethod
    def list_unread(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        """Return unread notifications for a recipient."""

    @abstractmethod
    def count_unread(self, recipient_id: UUID) -> int:
        """Return count of unread notifications for a recipient."""

    @abstractmethod
    def find(
        self, spec: NotificationFilter, page: PageRequest
    ) -> Sequence[Notification]:
        """Return notifications matching a filter."""

    @abstractmethod
    def mark_all_read(self, recipient_id: UUID) -> int:
        """Mark all pending/sent notifications as read. Returns count updated."""

    @abstractmethod
    def list_pending_for_delivery(self, limit: int) -> Sequence[Notification]:
        """Return pending notifications ready for outbound delivery."""