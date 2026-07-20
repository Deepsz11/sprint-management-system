"""SQLAlchemy implementation of the Notification repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.notification import Notification
from app.domain.enums import NotificationStatus
from app.domain.repositories.notification_repository import (
    NotificationRepositoryContract,
)
from app.domain.repositories.specifications import NotificationFilter, PageRequest
from app.infrastructure.persistence.mappers import NotificationMapper
from app.infrastructure.persistence.models.notification import NotificationModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyNotificationRepository(NotificationRepositoryContract):
    """SQLAlchemy implementation of the Notification repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Notification | None:
        model = self._session.get(NotificationModel, entity_id)
        return NotificationMapper.to_entity(model) if model else None

    def add(self, entity: Notification) -> Notification:
        model = NotificationMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return NotificationMapper.to_entity(model)

    def update(self, entity: Notification) -> Notification:
        model = self._session.get(NotificationModel, entity.id)
        if model is None:
            raise NotFoundError(f"Notification {entity.id} not found")
        NotificationMapper.to_model(entity, model)
        self._session.flush()
        return NotificationMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(NotificationModel, entity_id)
        if model is None:
            raise NotFoundError(f"Notification {entity_id} not found")
        self._session.delete(model)
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(NotificationModel).where(
            NotificationModel.id == entity_id
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_recipient(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        stmt = select(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id
        )
        stmt = apply_pagination(stmt, page, NotificationModel.created_at)
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_unread(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        stmt = select(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id,
            NotificationModel.status.in_(
                [NotificationStatus.PENDING.value, NotificationStatus.SENT.value]
            ),
        )
        stmt = apply_pagination(stmt, page, NotificationModel.created_at)
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_unread(self, recipient_id: UUID) -> int:
        stmt = select(func.count()).select_from(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id,
            NotificationModel.status.in_(
                [NotificationStatus.PENDING.value, NotificationStatus.SENT.value]
            ),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def find(
        self, spec: NotificationFilter, page: PageRequest
    ) -> Sequence[Notification]:
        stmt = select(NotificationModel)
        if spec.recipient_id:
            stmt = stmt.where(NotificationModel.recipient_id == spec.recipient_id)
        if spec.organization_id:
            stmt = stmt.where(NotificationModel.organization_id == spec.organization_id)
        if spec.statuses:
            stmt = stmt.where(NotificationModel.status.in_(spec.statuses))
        if spec.channels:
            stmt = stmt.where(NotificationModel.channel.in_(spec.channels))
        if spec.event_types:
            stmt = stmt.where(NotificationModel.event_type.in_(spec.event_types))
        stmt = apply_pagination(stmt, page, NotificationModel.created_at)
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def mark_all_read(self, recipient_id: UUID) -> int:
        now = utcnow()
        stmt = select(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id,
            NotificationModel.status.in_(
                [NotificationStatus.PENDING.value, NotificationStatus.SENT.value]
            ),
        )
        models = list(self._session.execute(stmt).scalars())
        for model in models:
            model.status = NotificationStatus.READ.value
            model.read_at = now
        self._session.flush()
        return len(models)

    def list_pending_for_delivery(self, limit: int) -> Sequence[Notification]:
        if limit <= 0:
            return []
        stmt = (
            select(NotificationModel)
            .where(NotificationModel.status == NotificationStatus.PENDING.value)
            .order_by(NotificationModel.created_at.asc())
            .limit(limit)
        )
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]