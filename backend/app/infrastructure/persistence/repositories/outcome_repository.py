"""SQLAlchemy implementation of the BusinessOutcome repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.enums import OutcomeStatus
from app.domain.repositories.outcome_repository import (
    BusinessOutcomeRepositoryContract,
)
from app.domain.repositories.specifications import OutcomeFilter, PageRequest
from app.infrastructure.persistence.mappers import BusinessOutcomeMapper
from app.infrastructure.persistence.models.business_outcome import BusinessOutcomeModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyBusinessOutcomeRepository(BusinessOutcomeRepositoryContract):
    """SQLAlchemy implementation of the BusinessOutcome repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> BusinessOutcome | None:
        model = self._session.get(BusinessOutcomeModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return BusinessOutcomeMapper.to_entity(model)

    def add(self, entity: BusinessOutcome) -> BusinessOutcome:
        model = BusinessOutcomeMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return BusinessOutcomeMapper.to_entity(model)

    def update(self, entity: BusinessOutcome) -> BusinessOutcome:
        model = self._session.get(BusinessOutcomeModel, entity.id)
        if model is None:
            raise NotFoundError(f"BusinessOutcome {entity.id} not found")
        BusinessOutcomeMapper.to_model(entity, model)
        self._session.flush()
        return BusinessOutcomeMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(BusinessOutcomeModel, entity_id)
        if model is None:
            raise NotFoundError(f"BusinessOutcome {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(BusinessOutcomeModel).where(
            BusinessOutcomeModel.id == entity_id,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = select(BusinessOutcomeModel).where(
            BusinessOutcomeModel.organization_id == organization_id,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = select(BusinessOutcomeModel).where(
            BusinessOutcomeModel.owner_id == owner_id,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_off_track(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        stmt = (
            select(BusinessOutcomeModel)
            .where(
                BusinessOutcomeModel.organization_id == organization_id,
                BusinessOutcomeModel.status == OutcomeStatus.OFF_TRACK.value,
                BusinessOutcomeModel.deleted_at.is_(None),
            )
            .order_by(BusinessOutcomeModel.target_date.asc().nulls_last())
        )
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_at_risk(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        stmt = (
            select(BusinessOutcomeModel)
            .where(
                BusinessOutcomeModel.organization_id == organization_id,
                BusinessOutcomeModel.status == OutcomeStatus.AT_RISK.value,
                BusinessOutcomeModel.deleted_at.is_(None),
            )
            .order_by(BusinessOutcomeModel.target_date.asc().nulls_last())
        )
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = select(BusinessOutcomeModel).where(
            BusinessOutcomeModel.organization_id == organization_id,
            BusinessOutcomeModel.status == OutcomeStatus.ACTIVE.value,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def _apply_filter(self, stmt: Select, spec: OutcomeFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(BusinessOutcomeModel.organization_id == spec.organization_id)
        if spec.owner_id:
            stmt = stmt.where(BusinessOutcomeModel.owner_id == spec.owner_id)
        if spec.statuses:
            stmt = stmt.where(BusinessOutcomeModel.status.in_(spec.statuses))
        if spec.target_before:
            stmt = stmt.where(BusinessOutcomeModel.target_date <= spec.target_before)
        if spec.target_after:
            stmt = stmt.where(BusinessOutcomeModel.target_date >= spec.target_after)
        if spec.search:
            pattern = f"%{spec.search.lower()}%"
            stmt = stmt.where(func.lower(BusinessOutcomeModel.name).like(pattern))
        if not spec.include_deleted:
            stmt = stmt.where(BusinessOutcomeModel.deleted_at.is_(None))
        return stmt

    def find(
        self, spec: OutcomeFilter, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = self._apply_filter(select(BusinessOutcomeModel), spec)
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count(self, spec: OutcomeFilter) -> int:
        stmt = self._apply_filter(
            select(func.count()).select_from(BusinessOutcomeModel), spec
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(BusinessOutcomeModel).where(
            BusinessOutcomeModel.organization_id == organization_id,
            func.lower(BusinessOutcomeModel.name) == name.lower(),
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(BusinessOutcomeModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0