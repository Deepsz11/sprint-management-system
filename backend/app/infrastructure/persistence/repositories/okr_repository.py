"""SQLAlchemy implementations of Objective and KeyResult repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.okr import KeyResult, Objective
from app.domain.enums import OKRStatus
from app.domain.repositories.okr_repository import (
    KeyResultRepositoryContract,
    ObjectiveRepositoryContract,
)
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.mappers import KeyResultMapper, ObjectiveMapper
from app.infrastructure.persistence.models.okr import KeyResultModel, ObjectiveModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyObjectiveRepository(ObjectiveRepositoryContract):
    """SQLAlchemy implementation of the Objective repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Objective | None:
        model = self._session.get(ObjectiveModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return ObjectiveMapper.to_entity(model)

    def add(self, entity: Objective) -> Objective:
        model = ObjectiveMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return ObjectiveMapper.to_entity(model)

    def update(self, entity: Objective) -> Objective:
        model = self._session.get(ObjectiveModel, entity.id)
        if model is None:
            raise NotFoundError(f"Objective {entity.id} not found")
        ObjectiveMapper.to_model(entity, model)
        self._session.flush()
        return ObjectiveMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(ObjectiveModel, entity_id)
        if model is None:
            raise NotFoundError(f"Objective {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(ObjectiveModel).where(
            ObjectiveModel.id == entity_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.organization_id == organization_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_team(
        self, team_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.team_id == team_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.owner_id == owner_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_parent(self, parent_id: UUID) -> Sequence[Objective]:
        stmt = (
            select(ObjectiveModel)
            .where(
                ObjectiveModel.parent_id == parent_id,
                ObjectiveModel.deleted_at.is_(None),
            )
            .order_by(ObjectiveModel.created_at.desc())
        )
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.organization_id == organization_id,
            ObjectiveModel.status == OKRStatus.ACTIVE.value,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_by_organization(self, organization_id: UUID) -> int:
        stmt = select(func.count()).select_from(ObjectiveModel).where(
            ObjectiveModel.organization_id == organization_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)


class SQLAlchemyKeyResultRepository(KeyResultRepositoryContract):
    """SQLAlchemy implementation of the KeyResult repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> KeyResult | None:
        model = self._session.get(KeyResultModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return KeyResultMapper.to_entity(model)

    def add(self, entity: KeyResult) -> KeyResult:
        model = KeyResultMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return KeyResultMapper.to_entity(model)

    def update(self, entity: KeyResult) -> KeyResult:
        model = self._session.get(KeyResultModel, entity.id)
        if model is None:
            raise NotFoundError(f"KeyResult {entity.id} not found")
        KeyResultMapper.to_model(entity, model)
        self._session.flush()
        return KeyResultMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(KeyResultModel, entity_id)
        if model is None:
            raise NotFoundError(f"KeyResult {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(KeyResultModel).where(
            KeyResultModel.id == entity_id,
            KeyResultModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_objective(self, objective_id: UUID) -> Sequence[KeyResult]:
        stmt = (
            select(KeyResultModel)
            .where(
                KeyResultModel.objective_id == objective_id,
                KeyResultModel.deleted_at.is_(None),
            )
            .order_by(KeyResultModel.created_at.asc())
        )
        return [
            KeyResultMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_kpi(self, kpi_id: UUID) -> Sequence[KeyResult]:
        stmt = (
            select(KeyResultModel)
            .where(
                KeyResultModel.kpi_id == kpi_id,
                KeyResultModel.deleted_at.is_(None),
            )
            .order_by(KeyResultModel.created_at.asc())
        )
        return [
            KeyResultMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_by_objective(self, objective_id: UUID) -> int:
        stmt = select(func.count()).select_from(KeyResultModel).where(
            KeyResultModel.objective_id == objective_id,
            KeyResultModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def delete_by_objective(self, objective_id: UUID) -> int:
        now = utcnow()
        stmt = (
            select(KeyResultModel)
            .where(
                KeyResultModel.objective_id == objective_id,
                KeyResultModel.deleted_at.is_(None),
            )
        )
        models = list(self._session.execute(stmt).scalars())
        for model in models:
            model.deleted_at = now
        self._session.flush()
        return len(models)