"""SQLAlchemy implementation of the Project repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.project import Project
from app.domain.repositories.project_repository import ProjectRepositoryContract
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.mappers import ProjectMapper
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyProjectRepository(ProjectRepositoryContract):
    """SQLAlchemy implementation of the Project repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Project | None:
        model = self._session.get(ProjectModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return ProjectMapper.to_entity(model)

    def add(self, entity: Project) -> Project:
        model = ProjectMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return ProjectMapper.to_entity(model)

    def update(self, entity: Project) -> Project:
        model = self._session.get(ProjectModel, entity.id)
        if model is None:
            raise NotFoundError(f"Project {entity.id} not found")
        ProjectMapper.to_model(entity, model)
        self._session.flush()
        return ProjectMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(ProjectModel, entity_id)
        if model is None:
            raise NotFoundError(f"Project {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.id == entity_id,
            ProjectModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_key(self, organization_id: UUID, key: str) -> Project | None:
        stmt = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.key == key.upper(),
            ProjectModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return ProjectMapper.to_entity(model) if model else None

    def get_by_slug(self, organization_id: UUID, slug: str) -> Project | None:
        stmt = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.slug == slug.lower(),
            ProjectModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return ProjectMapper.to_entity(model) if model else None

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        stmt = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.deleted_at.is_(None),
        )
        if not include_archived:
            stmt = stmt.where(ProjectModel.is_archived.is_(False))
        stmt = apply_pagination(stmt, page, ProjectModel.created_at)
        return [ProjectMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_team(
        self, team_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        stmt = select(ProjectModel).where(
            ProjectModel.team_id == team_id,
            ProjectModel.deleted_at.is_(None),
        )
        if not include_archived:
            stmt = stmt.where(ProjectModel.is_archived.is_(False))
        stmt = apply_pagination(stmt, page, ProjectModel.created_at)
        return [ProjectMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def key_exists(
        self, organization_id: UUID, key: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.key == key.upper(),
            ProjectModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(ProjectModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.slug == slug.lower(),
            ProjectModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(ProjectModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def count_by_organization(
        self, organization_id: UUID, include_archived: bool = False
    ) -> int:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.deleted_at.is_(None),
        )
        if not include_archived:
            stmt = stmt.where(ProjectModel.is_archived.is_(False))
        return int(self._session.execute(stmt).scalar_one() or 0)