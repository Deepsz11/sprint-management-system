"""SQLAlchemy implementation of the Sprint repository."""

from __future__ import annotations

from datetime import date
from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.sprint import Sprint
from app.domain.enums import SprintStatus
from app.domain.repositories.specifications import PageRequest, SprintFilter
from app.domain.repositories.sprint_repository import SprintRepositoryContract
from app.infrastructure.persistence.mappers import SprintMapper
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.models.sprint import SprintModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemySprintRepository(SprintRepositoryContract):
    """SQLAlchemy implementation of the Sprint repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Sprint | None:
        model = self._session.get(SprintModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return SprintMapper.to_entity(model)

    def add(self, entity: Sprint) -> Sprint:
        model = SprintMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return SprintMapper.to_entity(model)

    def update(self, entity: Sprint) -> Sprint:
        model = self._session.get(SprintModel, entity.id)
        if model is None:
            raise NotFoundError(f"Sprint {entity.id} not found")
        SprintMapper.to_model(entity, model)
        self._session.flush()
        return SprintMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(SprintModel, entity_id)
        if model is None:
            raise NotFoundError(f"Sprint {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(SprintModel).where(
            SprintModel.id == entity_id,
            SprintModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_project(self, project_id: UUID, page: PageRequest) -> Sequence[Sprint]:
        stmt = select(SprintModel).where(
            SprintModel.project_id == project_id,
            SprintModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, SprintModel.start_date)
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def get_active_for_project(self, project_id: UUID) -> Sprint | None:
        stmt = select(SprintModel).where(
            SprintModel.project_id == project_id,
            SprintModel.status == SprintStatus.ACTIVE.value,
            SprintModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return SprintMapper.to_entity(model) if model else None

    def list_completed_in_range(
        self, organization_id: UUID, start: date, end: date
    ) -> Sequence[Sprint]:
        stmt = (
            select(SprintModel)
            .join(ProjectModel, ProjectModel.id == SprintModel.project_id)
            .where(
                ProjectModel.organization_id == organization_id,
                SprintModel.status == SprintStatus.COMPLETED.value,
                SprintModel.end_date >= start,
                SprintModel.end_date <= end,
                SprintModel.deleted_at.is_(None),
            )
            .order_by(SprintModel.end_date.desc())
        )
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_active_for_organization(
        self, organization_id: UUID
    ) -> Sequence[Sprint]:
        stmt = (
            select(SprintModel)
            .join(ProjectModel, ProjectModel.id == SprintModel.project_id)
            .where(
                ProjectModel.organization_id == organization_id,
                SprintModel.status == SprintStatus.ACTIVE.value,
                SprintModel.deleted_at.is_(None),
            )
            .order_by(SprintModel.start_date.desc())
        )
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: SprintFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.join(ProjectModel, ProjectModel.id == SprintModel.project_id).where(
                ProjectModel.organization_id == spec.organization_id
            )
        if spec.project_id:
            stmt = stmt.where(SprintModel.project_id == spec.project_id)
        if spec.statuses:
            stmt = stmt.where(SprintModel.status.in_(spec.statuses))
        if spec.starts_after:
            stmt = stmt.where(SprintModel.start_date >= spec.starts_after)
        if spec.ends_before:
            stmt = stmt.where(SprintModel.end_date <= spec.ends_before)
        if not spec.include_deleted:
            stmt = stmt.where(SprintModel.deleted_at.is_(None))
        return stmt

    def find(self, spec: SprintFilter, page: PageRequest) -> Sequence[Sprint]:
        stmt = self._apply_filter(select(SprintModel), spec)
        stmt = apply_pagination(stmt, page, SprintModel.start_date)
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: SprintFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(SprintModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)

    def latest_by_project(self, project_id: UUID, limit: int = 5) -> Sequence[Sprint]:
        if limit <= 0:
            return []
        stmt = (
            select(SprintModel)
            .where(
                SprintModel.project_id == project_id,
                SprintModel.deleted_at.is_(None),
            )
            .order_by(SprintModel.start_date.desc())
            .limit(limit)
        )
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]