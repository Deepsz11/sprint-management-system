"""SQLAlchemy implementations of User and TeamMembership repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.user import TeamMembership, User
from app.domain.repositories.specifications import PageRequest
from app.domain.repositories.user_repository import (
    TeamMembershipRepositoryContract,
    UserRepositoryContract,
)
from app.infrastructure.persistence.mappers import (
    TeamMembershipMapper,
    UserMapper,
)
from app.infrastructure.persistence.models.user import (
    TeamMembershipModel,
    UserModel,
)
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyUserRepository(UserRepositoryContract):
    """SQLAlchemy implementation of the User repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> User | None:
        model = self._session.get(UserModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return UserMapper.to_entity(model)

    def add(self, entity: User) -> User:
        model = UserMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return UserMapper.to_entity(model)

    def update(self, entity: User) -> User:
        model = self._session.get(UserModel, entity.id)
        if model is None:
            raise NotFoundError(f"User {entity.id} not found")
        UserMapper.to_model(entity, model)
        self._session.flush()
        return UserMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(UserModel, entity_id)
        if model is None:
            raise NotFoundError(f"User {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(UserModel).where(
            UserModel.id == entity_id,
            UserModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(
            func.lower(UserModel.email) == email.lower(),
            UserModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    def email_exists(self, email: str, exclude_id: UUID | None = None) -> bool:
        stmt = select(func.count()).select_from(UserModel).where(
            func.lower(UserModel.email) == email.lower(),
            UserModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(UserModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[User]:
        stmt = select(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, UserModel.created_at)
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_team(self, team_id: UUID) -> Sequence[User]:
        stmt = (
            select(UserModel)
            .join(TeamMembershipModel, TeamMembershipModel.user_id == UserModel.id)
            .where(
                TeamMembershipModel.team_id == team_id,
                TeamMembershipModel.deleted_at.is_(None),
                UserModel.deleted_at.is_(None),
            )
            .order_by(UserModel.full_name.asc())
        )
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_role(
        self, organization_id: UUID, role: str, page: PageRequest
    ) -> Sequence[User]:
        stmt = select(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.role == role,
            UserModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, UserModel.created_at)
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def search(
        self, organization_id: UUID, query: str, page: PageRequest
    ) -> Sequence[User]:
        pattern = f"%{query.lower()}%"
        stmt = select(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.deleted_at.is_(None),
            or_(
                func.lower(UserModel.email).like(pattern),
                func.lower(UserModel.full_name).like(pattern),
            ),
        )
        stmt = apply_pagination(stmt, page, UserModel.full_name)
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count_by_organization(self, organization_id: UUID) -> int:
        stmt = select(func.count()).select_from(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)


class SQLAlchemyTeamMembershipRepository(TeamMembershipRepositoryContract):
    """SQLAlchemy implementation of the TeamMembership repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> TeamMembership | None:
        model = self._session.get(TeamMembershipModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return TeamMembershipMapper.to_entity(model)

    def add(self, entity: TeamMembership) -> TeamMembership:
        model = TeamMembershipMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return TeamMembershipMapper.to_entity(model)

    def update(self, entity: TeamMembership) -> TeamMembership:
        model = self._session.get(TeamMembershipModel, entity.id)
        if model is None:
            raise NotFoundError(f"TeamMembership {entity.id} not found")
        TeamMembershipMapper.to_model(entity, model)
        self._session.flush()
        return TeamMembershipMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(TeamMembershipModel, entity_id)
        if model is None:
            raise NotFoundError(f"TeamMembership {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(TeamMembershipModel).where(
            TeamMembershipModel.id == entity_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_team_and_user(
        self, team_id: UUID, user_id: UUID
    ) -> TeamMembership | None:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.team_id == team_id,
            TeamMembershipModel.user_id == user_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return TeamMembershipMapper.to_entity(model) if model else None

    def list_by_team(self, team_id: UUID) -> Sequence[TeamMembership]:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.team_id == team_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        return [
            TeamMembershipMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_user(self, user_id: UUID) -> Sequence[TeamMembership]:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.user_id == user_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        return [
            TeamMembershipMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def remove_by_team_and_user(self, team_id: UUID, user_id: UUID) -> None:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.team_id == team_id,
            TeamMembershipModel.user_id == user_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        if model is None:
            raise NotFoundError("Team membership not found")
        model.deleted_at = utcnow()
        self._session.flush()