"""SQLAlchemy implementations of KPI and MetricSnapshot repositories."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, delete, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.kpi import KPI, MetricSnapshot
from app.domain.repositories.kpi_repository import (
    KPIRepositoryContract,
    MetricSnapshotRepositoryContract,
)
from app.domain.repositories.specifications import (
    KPIFilter,
    MetricSnapshotFilter,
    PageRequest,
)
from app.infrastructure.persistence.mappers import KPIMapper, MetricSnapshotMapper
from app.infrastructure.persistence.models.kpi import KPIModel, MetricSnapshotModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyKPIRepository(KPIRepositoryContract):
    """SQLAlchemy implementation of the KPI repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> KPI | None:
        model = self._session.get(KPIModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return KPIMapper.to_entity(model)

    def add(self, entity: KPI) -> KPI:
        model = KPIMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return KPIMapper.to_entity(model)

    def update(self, entity: KPI) -> KPI:
        model = self._session.get(KPIModel, entity.id)
        if model is None:
            raise NotFoundError(f"KPI {entity.id} not found")
        KPIMapper.to_model(entity, model)
        self._session.flush()
        return KPIMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(KPIModel, entity_id)
        if model is None:
            raise NotFoundError(f"KPI {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(KPIModel).where(
            KPIModel.id == entity_id,
            KPIModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.organization_id == organization_id,
            KPIModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_outcome(self, outcome_id: UUID) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.outcome_id == outcome_id,
            KPIModel.deleted_at.is_(None),
        ).order_by(KPIModel.name.asc())
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_owner(self, owner_id: UUID, page: PageRequest) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.owner_id == owner_id,
            KPIModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_active(self, organization_id: UUID, page: PageRequest) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.organization_id == organization_id,
            KPIModel.is_active.is_(True),
            KPIModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: KPIFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(KPIModel.organization_id == spec.organization_id)
        if spec.outcome_id:
            stmt = stmt.where(KPIModel.outcome_id == spec.outcome_id)
        if spec.owner_id:
            stmt = stmt.where(KPIModel.owner_id == spec.owner_id)
        if spec.units:
            stmt = stmt.where(KPIModel.unit.in_(spec.units))
        if spec.is_active is not None:
            stmt = stmt.where(KPIModel.is_active.is_(spec.is_active))
        if not spec.include_deleted:
            stmt = stmt.where(KPIModel.deleted_at.is_(None))
        return stmt

    def find(self, spec: KPIFilter, page: PageRequest) -> Sequence[KPI]:
        stmt = self._apply_filter(select(KPIModel), spec)
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: KPIFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(KPIModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)

    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(KPIModel).where(
            KPIModel.organization_id == organization_id,
            func.lower(KPIModel.name) == name.lower(),
            KPIModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(KPIModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0


class SQLAlchemyMetricSnapshotRepository(MetricSnapshotRepositoryContract):
    """SQLAlchemy implementation of the MetricSnapshot repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> MetricSnapshot | None:
        model = self._session.get(MetricSnapshotModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return MetricSnapshotMapper.to_entity(model)

    def add(self, entity: MetricSnapshot) -> MetricSnapshot:
        model = MetricSnapshotMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return MetricSnapshotMapper.to_entity(model)

    def update(self, entity: MetricSnapshot) -> MetricSnapshot:
        model = self._session.get(MetricSnapshotModel, entity.id)
        if model is None:
            raise NotFoundError(f"MetricSnapshot {entity.id} not found")
        MetricSnapshotMapper.to_model(entity, model)
        self._session.flush()
        return MetricSnapshotMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(MetricSnapshotModel, entity_id)
        if model is None:
            raise NotFoundError(f"MetricSnapshot {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(MetricSnapshotModel).where(
            MetricSnapshotModel.id == entity_id,
            MetricSnapshotModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_kpi(
        self, kpi_id: UUID, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        stmt = select(MetricSnapshotModel).where(
            MetricSnapshotModel.kpi_id == kpi_id,
            MetricSnapshotModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, MetricSnapshotModel.recorded_at)
        return [
            MetricSnapshotMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def latest_for_kpi(self, kpi_id: UUID) -> MetricSnapshot | None:
        stmt = (
            select(MetricSnapshotModel)
            .where(
                MetricSnapshotModel.kpi_id == kpi_id,
                MetricSnapshotModel.deleted_at.is_(None),
            )
            .order_by(MetricSnapshotModel.recorded_at.desc())
            .limit(1)
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return MetricSnapshotMapper.to_entity(model) if model else None

    def list_in_range(
        self, kpi_id: UUID, start: datetime, end: datetime
    ) -> Sequence[MetricSnapshot]:
        stmt = (
            select(MetricSnapshotModel)
            .where(
                MetricSnapshotModel.kpi_id == kpi_id,
                MetricSnapshotModel.recorded_at >= start,
                MetricSnapshotModel.recorded_at <= end,
                MetricSnapshotModel.deleted_at.is_(None),
            )
            .order_by(MetricSnapshotModel.recorded_at.asc())
        )
        return [
            MetricSnapshotMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def find(
        self, spec: MetricSnapshotFilter, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        stmt = select(MetricSnapshotModel).where(MetricSnapshotModel.deleted_at.is_(None))
        if spec.kpi_id:
            stmt = stmt.where(MetricSnapshotModel.kpi_id == spec.kpi_id)
        if spec.recorded_after:
            stmt = stmt.where(MetricSnapshotModel.recorded_at >= spec.recorded_after)
        if spec.recorded_before:
            stmt = stmt.where(MetricSnapshotModel.recorded_at <= spec.recorded_before)
        if spec.source:
            stmt = stmt.where(MetricSnapshotModel.source == spec.source)
        stmt = apply_pagination(stmt, page, MetricSnapshotModel.recorded_at)
        return [
            MetricSnapshotMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def delete_older_than(self, kpi_id: UUID, cutoff: datetime) -> int:
        stmt = delete(MetricSnapshotModel).where(
            MetricSnapshotModel.kpi_id == kpi_id,
            MetricSnapshotModel.recorded_at < cutoff,
        )
        result = self._session.execute(stmt)
        return int(result.rowcount or 0)