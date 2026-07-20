"""SQLAlchemy implementations of Attribution and Evidence repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.attribution import Evidence, OutcomeAttribution
from app.domain.repositories.attribution_repository import (
    AttributionRepositoryContract,
    EvidenceRepositoryContract,
)
from app.domain.repositories.specifications import AttributionFilter, PageRequest
from app.infrastructure.persistence.mappers import AttributionMapper, EvidenceMapper
from app.infrastructure.persistence.models.attribution import (
    EvidenceModel,
    OutcomeAttributionModel,
)
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyAttributionRepository(AttributionRepositoryContract):
    """SQLAlchemy implementation of the OutcomeAttribution repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> OutcomeAttribution | None:
        model = self._session.get(OutcomeAttributionModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return AttributionMapper.to_entity(model)

    def add(self, entity: OutcomeAttribution) -> OutcomeAttribution:
        model = AttributionMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return AttributionMapper.to_entity(model)

    def update(self, entity: OutcomeAttribution) -> OutcomeAttribution:
        model = self._session.get(OutcomeAttributionModel, entity.id)
        if model is None:
            raise NotFoundError(f"Attribution {entity.id} not found")
        AttributionMapper.to_model(entity, model)
        self._session.flush()
        return AttributionMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(OutcomeAttributionModel, entity_id)
        if model is None:
            raise NotFoundError(f"Attribution {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(OutcomeAttributionModel).where(
            OutcomeAttributionModel.id == entity_id,
            OutcomeAttributionModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_work_item(self, work_item_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.work_item_id == work_item_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_sprint(self, sprint_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.sprint_id == sprint_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_outcome(self, outcome_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.outcome_id == outcome_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_kpi(self, kpi_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.kpi_id == kpi_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_key_result(
        self, key_result_id: UUID
    ) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.key_result_id == key_result_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        stmt = select(OutcomeAttributionModel).where(
            OutcomeAttributionModel.organization_id == organization_id,
            OutcomeAttributionModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, OutcomeAttributionModel.created_at)
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def _apply_filter(self, stmt: Select, spec: AttributionFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(OutcomeAttributionModel.organization_id == spec.organization_id)
        if spec.work_item_id:
            stmt = stmt.where(OutcomeAttributionModel.work_item_id == spec.work_item_id)
        if spec.sprint_id:
            stmt = stmt.where(OutcomeAttributionModel.sprint_id == spec.sprint_id)
        if spec.outcome_id:
            stmt = stmt.where(OutcomeAttributionModel.outcome_id == spec.outcome_id)
        if spec.kpi_id:
            stmt = stmt.where(OutcomeAttributionModel.kpi_id == spec.kpi_id)
        if spec.key_result_id:
            stmt = stmt.where(OutcomeAttributionModel.key_result_id == spec.key_result_id)
        if spec.strengths:
            stmt = stmt.where(OutcomeAttributionModel.strength.in_(spec.strengths))
        if spec.methods:
            stmt = stmt.where(OutcomeAttributionModel.method.in_(spec.methods))
        if not spec.include_deleted:
            stmt = stmt.where(OutcomeAttributionModel.deleted_at.is_(None))
        return stmt

    def find(
        self, spec: AttributionFilter, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        stmt = self._apply_filter(select(OutcomeAttributionModel), spec)
        stmt = apply_pagination(stmt, page, OutcomeAttributionModel.created_at)
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count(self, spec: AttributionFilter) -> int:
        stmt = self._apply_filter(
            select(func.count()).select_from(OutcomeAttributionModel), spec
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def exists_for_pair(
        self,
        work_item_id: UUID | None,
        sprint_id: UUID | None,
        outcome_id: UUID | None,
        kpi_id: UUID | None,
        key_result_id: UUID | None,
    ) -> bool:
        stmt = select(func.count()).select_from(OutcomeAttributionModel).where(
            OutcomeAttributionModel.deleted_at.is_(None)
        )
        stmt = stmt.where(
            OutcomeAttributionModel.work_item_id.is_(None)
            if work_item_id is None
            else OutcomeAttributionModel.work_item_id == work_item_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.sprint_id.is_(None)
            if sprint_id is None
            else OutcomeAttributionModel.sprint_id == sprint_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.outcome_id.is_(None)
            if outcome_id is None
            else OutcomeAttributionModel.outcome_id == outcome_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.kpi_id.is_(None)
            if kpi_id is None
            else OutcomeAttributionModel.kpi_id == kpi_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.key_result_id.is_(None)
            if key_result_id is None
            else OutcomeAttributionModel.key_result_id == key_result_id
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0


class SQLAlchemyEvidenceRepository(EvidenceRepositoryContract):
    """SQLAlchemy implementation of the Evidence repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Evidence | None:
        model = self._session.get(EvidenceModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return EvidenceMapper.to_entity(model)

    def add(self, entity: Evidence) -> Evidence:
        model = EvidenceMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return EvidenceMapper.to_entity(model)

    def update(self, entity: Evidence) -> Evidence:
        model = self._session.get(EvidenceModel, entity.id)
        if model is None:
            raise NotFoundError(f"Evidence {entity.id} not found")
        EvidenceMapper.to_model(entity, model)
        self._session.flush()
        return EvidenceMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(EvidenceModel, entity_id)
        if model is None:
            raise NotFoundError(f"Evidence {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(EvidenceModel).where(
            EvidenceModel.id == entity_id,
            EvidenceModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_attribution(self, attribution_id: UUID) -> Sequence[Evidence]:
        stmt = (
            select(EvidenceModel)
            .where(
                EvidenceModel.attribution_id == attribution_id,
                EvidenceModel.deleted_at.is_(None),
            )
            .order_by(EvidenceModel.created_at.desc())
        )
        return [
            EvidenceMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_by_attribution(self, attribution_id: UUID) -> int:
        stmt = select(func.count()).select_from(EvidenceModel).where(
            EvidenceModel.attribution_id == attribution_id,
            EvidenceModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def delete_by_attribution(self, attribution_id: UUID) -> int:
        now = utcnow()
        stmt = select(EvidenceModel).where(
            EvidenceModel.attribution_id == attribution_id,
            EvidenceModel.deleted_at.is_(None),
        )
        models = list(self._session.execute(stmt).scalars())
        for model in models:
            model.deleted_at = now
        self._session.flush()
        return len(models)