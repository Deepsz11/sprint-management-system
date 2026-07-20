"""SQLAlchemy implementations of Organization and Team repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.organization import Organization, Team
from app.domain.repositories.organization_repository import (
    OrganizationRepositoryContract,
    TeamRepositoryContract,
)
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.mappers import OrganizationMapper, TeamMapper
from app.infrastructure.persistence.models.organization import (
    OrganizationModel,
    TeamModel,
)
from app.infrastructure.persistence.models.user import TeamMembershipModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyOrganizationRepository(OrganizationRepositoryContract):
    """SQLAlchemy implementation of the Organization repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Organization | None:
        model = self._session.get(OrganizationModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return OrganizationMapper.to_entity(model)

    def add(self, entity: Organization) -> Organization:
        model = OrganizationMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return OrganizationMapper.to_entity(model)

    def update(self, entity: Organization) -> Organization:
        model = self._session.get(OrganizationModel, entity.id)
        if model is None:
            raise NotFoundError(f"Organization {entity.id} not found")
        OrganizationMapper.to_model(entity, model)
        self._session.flush()
        return OrganizationMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(OrganizationModel, entity_id)
        if model is None:
            raise NotFoundError(f"Organization {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).where(
            OrganizationModel.id == entity_id,
            OrganizationModel.deleted_at.is_(None),
        )
        return (self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_slug(self, slug: str) -> Organization | None:
        stmt = select(OrganizationModel).where(
            OrganizationModel.slug == slug.lower(),
            OrganizationModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return OrganizationMapper.to_entity(model) if model else None

    def get_by_billing_email(self, email: str) -> Organization | None:
        stmt = select(OrganizationModel).where(
            func.lower(OrganizationModel.billing_email) == email.lower(),
            OrganizationModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return OrganizationMapper.to_entity(model) if model else None

    def list_all(self, page: PageRequest) -> Sequence[Organization]:
        stmt = select(OrganizationModel).where(OrganizationModel.deleted_at.is_(None))
        stmt = apply_pagination(stmt, page, OrganizationModel.created_at)
        return [OrganizationMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_active(self, page: PageRequest) -> Sequence[Organization]:
        stmt = select(OrganizationModel).where(
            OrganizationModel.deleted_at.is_(None),
            OrganizationModel.is_active.is_(True),
        )
        stmt = apply_pagination(stmt, page, OrganizationModel.created_at)
        return [OrganizationMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self) -> int:
        stmt = select(func.count()).select_from(OrganizationModel).where(
            OrganizationModel.deleted_at.is_(None)
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        stmt = select(func.count()).select_from(OrganizationModel).where(
            OrganizationModel.slug == slug.lower(),
            OrganizationModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(OrganizationModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0


class SQLAlchemyTeamRepository(TeamRepositoryContract):
    """SQLAlchemy implementation of the Team repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Team | None:
        model = self._session.get(TeamModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return TeamMapper.to_entity(model)

    def add(self, entity: Team) -> Team:
        model = TeamMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return TeamMapper.to_entity(model)

    def update(self, entity: Team) -> Team:
        model = self._session.get(TeamModel, entity.id)
        if model is None:
            raise NotFoundError(f"Team {entity.id} not found")
        TeamMapper.to_model(entity, model)
        self._session.flush()
        return TeamMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(TeamModel, entity_id)
        if model is None:
            raise NotFoundError(f"Team {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(TeamModel).where(
            TeamModel.id == entity_id,
            TeamModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_slug(self, organization_id: UUID, slug: str) -> Team | None:
        stmt = select(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.slug == slug.lower(),
            TeamModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return TeamMapper.to_entity(model) if model else None

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Team]:
        stmt = select(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, TeamModel.created_at)
        return [TeamMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_user(self, user_id: UUID) -> Sequence[Team]:
        stmt = (
            select(TeamModel)
            .join(TeamMembershipModel, TeamMembershipModel.team_id == TeamModel.id)
            .where(
                TeamMembershipModel.user_id == user_id,
                TeamMembershipModel.deleted_at.is_(None),
                TeamModel.deleted_at.is_(None),
            )
            .order_by(TeamModel.name.asc())
        )
        return [TeamMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count_by_organization(self, organization_id: UUID) -> int:
        stmt = select(func.count()).select_from(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.slug == slug.lower(),
            TeamModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(TeamModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0