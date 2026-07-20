"""SQLAlchemy implementation of the WorkItem repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select, update
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.work_item import WorkItem
from app.domain.enums import WorkItemStatus
from app.domain.repositories.specifications import PageRequest, WorkItemFilter
from app.domain.repositories.work_item_repository import WorkItemRepositoryContract
from app.infrastructure.persistence.mappers import WorkItemMapper
from app.infrastructure.persistence.models.attribution import OutcomeAttributionModel
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.models.work_item import WorkItemModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyWorkItemRepository(WorkItemRepositoryContract):
    """SQLAlchemy implementation of the WorkItem repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> WorkItem | None:
        model = self._session.get(WorkItemModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return WorkItemMapper.to_entity(model)

    def add(self, entity: WorkItem) -> WorkItem:
        model = WorkItemMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return WorkItemMapper.to_entity(model)

    def update(self, entity: WorkItem) -> WorkItem:
        model = self._session.get(WorkItemModel, entity.id)
        if model is None:
            raise NotFoundError(f"WorkItem {entity.id} not found")
        WorkItemMapper.to_model(entity, model)
        self._session.flush()
        return WorkItemMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(WorkItemModel, entity_id)
        if model is None:
            raise NotFoundError(f"WorkItem {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(WorkItemModel).where(
            WorkItemModel.id == entity_id,
            WorkItemModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_external_key(
        self, project_id: UUID, external_key: str
    ) -> WorkItem | None:
        stmt = select(WorkItemModel).where(
            WorkItemModel.project_id == project_id,
            WorkItemModel.external_key == external_key,
            WorkItemModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return WorkItemMapper.to_entity(model) if model else None

    def list_by_sprint(self, sprint_id: UUID) -> Sequence[WorkItem]:
        stmt = (
            select(WorkItemModel)
            .where(
                WorkItemModel.sprint_id == sprint_id,
                WorkItemModel.deleted_at.is_(None),
            )
            .order_by(WorkItemModel.created_at.desc())
        )
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_project(
        self, project_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        stmt = select(WorkItemModel).where(
            WorkItemModel.project_id == project_id,
            WorkItemModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, WorkItemModel.created_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_epic(self, epic_id: UUID) -> Sequence[WorkItem]:
        stmt = (
            select(WorkItemModel)
            .where(
                WorkItemModel.epic_id == epic_id,
                WorkItemModel.deleted_at.is_(None),
            )
            .order_by(WorkItemModel.created_at.desc())
        )
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_parent(self, parent_id: UUID) -> Sequence[WorkItem]:
        stmt = (
            select(WorkItemModel)
            .where(
                WorkItemModel.parent_id == parent_id,
                WorkItemModel.deleted_at.is_(None),
            )
            .order_by(WorkItemModel.created_at.desc())
        )
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_assignee(
        self, user_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        stmt = select(WorkItemModel).where(
            WorkItemModel.assignee_id == user_id,
            WorkItemModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, WorkItemModel.created_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_unattributed(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        subq = (
            select(OutcomeAttributionModel.work_item_id)
            .where(
                OutcomeAttributionModel.work_item_id.is_not(None),
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .subquery()
        )
        stmt = (
            select(WorkItemModel)
            .join(ProjectModel, ProjectModel.id == WorkItemModel.project_id)
            .where(
                ProjectModel.organization_id == organization_id,
                WorkItemModel.status == WorkItemStatus.DONE.value,
                WorkItemModel.deleted_at.is_(None),
                WorkItemModel.id.not_in(select(subq.c.work_item_id)),
            )
        )
        stmt = apply_pagination(stmt, page, WorkItemModel.completed_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: WorkItemFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.join(ProjectModel, ProjectModel.id == WorkItemModel.project_id).where(
                ProjectModel.organization_id == spec.organization_id
            )
        if spec.project_id:
            stmt = stmt.where(WorkItemModel.project_id == spec.project_id)
        if spec.sprint_id:
            stmt = stmt.where(WorkItemModel.sprint_id == spec.sprint_id)
        if spec.assignee_id:
            stmt = stmt.where(WorkItemModel.assignee_id == spec.assignee_id)
        if spec.reporter_id:
            stmt = stmt.where(WorkItemModel.reporter_id == spec.reporter_id)
        if spec.epic_id:
            stmt = stmt.where(WorkItemModel.epic_id == spec.epic_id)
        if spec.item_types:
            stmt = stmt.where(WorkItemModel.item_type.in_(spec.item_types))
        if spec.statuses:
            stmt = stmt.where(WorkItemModel.status.in_(spec.statuses))
        if spec.priorities:
            stmt = stmt.where(WorkItemModel.priority.in_(spec.priorities))
        if spec.labels:
            stmt = stmt.where(WorkItemModel.labels.op("&&")(list(spec.labels)))
        if spec.search:
            pattern = f"%{spec.search.lower()}%"
            stmt = stmt.where(func.lower(WorkItemModel.title).like(pattern))
        if spec.completed_after:
            stmt = stmt.where(WorkItemModel.completed_at >= spec.completed_after)
        if spec.completed_before:
            stmt = stmt.where(WorkItemModel.completed_at <= spec.completed_before)
        if not spec.include_deleted:
            stmt = stmt.where(WorkItemModel.deleted_at.is_(None))
        return stmt

    def find(self, spec: WorkItemFilter, page: PageRequest) -> Sequence[WorkItem]:
        stmt = self._apply_filter(select(WorkItemModel), spec)
        stmt = apply_pagination(stmt, page, WorkItemModel.created_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: WorkItemFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(WorkItemModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)

    def bulk_reassign_sprint(
        self, work_item_ids: Sequence[UUID], sprint_id: UUID | None
    ) -> int:
        if not work_item_ids:
            return 0
        stmt = (
            update(WorkItemModel)
            .where(
                WorkItemModel.id.in_(list(work_item_ids)),
                WorkItemModel.deleted_at.is_(None),
            )
            .values(sprint_id=sprint_id, updated_at=utcnow())
        )
        result = self._session.execute(stmt)
        return int(result.rowcount or 0)