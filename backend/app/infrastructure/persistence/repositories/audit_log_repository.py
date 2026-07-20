"""SQLAlchemy implementation of the AuditLog repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.audit_log_repository import AuditLogRepositoryContract
from app.domain.repositories.specifications import AuditLogFilter, PageRequest
from app.infrastructure.persistence.mappers import AuditLogMapper
from app.infrastructure.persistence.models.audit_log import AuditLogModel
from app.infrastructure.persistence.repositories._base import apply_pagination


class SQLAlchemyAuditLogRepository(AuditLogRepositoryContract):
    """SQLAlchemy implementation of the AuditLog repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> AuditLog | None:
        model = self._session.get(AuditLogModel, entity_id)
        return AuditLogMapper.to_entity(model) if model else None

    def add(self, entity: AuditLog) -> AuditLog:
        model = AuditLogMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return AuditLogMapper.to_entity(model)

    def update(self, entity: AuditLog) -> AuditLog:
        raise NotFoundError("Audit logs are immutable and cannot be updated")

    def delete(self, entity_id: UUID) -> None:
        raise NotFoundError("Audit logs are immutable and cannot be deleted")

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(AuditLogModel).where(
            AuditLogModel.id == entity_id
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLogModel).where(
            AuditLogModel.organization_id == organization_id
        )
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_resource(
        self, resource_type: str, resource_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLogModel).where(
            AuditLogModel.resource_type == resource_type,
            AuditLogModel.resource_id == resource_id,
        )
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_actor(
        self, actor_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLogModel).where(AuditLogModel.actor_id == actor_id)
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: AuditLogFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(AuditLogModel.organization_id == spec.organization_id)
        if spec.actor_id:
            stmt = stmt.where(AuditLogModel.actor_id == spec.actor_id)
        if spec.resource_type:
            stmt = stmt.where(AuditLogModel.resource_type == spec.resource_type)
        if spec.resource_id:
            stmt = stmt.where(AuditLogModel.resource_id == spec.resource_id)
        if spec.actions:
            stmt = stmt.where(AuditLogModel.action.in_(spec.actions))
        if spec.occurred_after:
            stmt = stmt.where(AuditLogModel.created_at >= spec.occurred_after)
        if spec.occurred_before:
            stmt = stmt.where(AuditLogModel.created_at <= spec.occurred_before)
        return stmt

    def find(self, spec: AuditLogFilter, page: PageRequest) -> Sequence[AuditLog]:
        stmt = self._apply_filter(select(AuditLogModel), spec)
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: AuditLogFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(AuditLogModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)