"""List KPI snapshot history use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi_extensions import KPIHistoryDTO
from app.application.mappers import kpi_to_dto, metric_snapshot_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.repositories.specifications import (
    MetricSnapshotFilter,
    PageRequest,
)
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListKPIHistoryQuery:
    """Filter + pagination query for KPI history."""

    kpi_id: UUID
    context: RequestContext
    limit: int = 100
    offset: int = 0
    recorded_after: datetime | None = None
    recorded_before: datetime | None = None
    source: str | None = None


class ListKPIHistoryUseCase(UseCase[ListKPIHistoryQuery, KPIHistoryDTO]):
    """Return the historical snapshots for a KPI."""

    def execute(self, query: ListKPIHistoryQuery) -> KPIHistoryDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.KPI_READ)

        if query.limit <= 0 or query.limit > 1000:
            raise ValidationError("limit must be between 1 and 1000")
        if query.offset < 0:
            raise ValidationError("offset cannot be negative")

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(query.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {query.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, kpi.organization_id
            )

            spec = MetricSnapshotFilter(
                kpi_id=kpi.id,
                recorded_after=query.recorded_after,
                recorded_before=query.recorded_before,
                source=query.source,
            )
            page = PageRequest(
                limit=query.limit,
                offset=query.offset,
                order_by="recorded_at",
                descending=True,
            )
            snapshots = uow.metric_snapshots.find(spec, page)

            snapshot_dtos = [metric_snapshot_to_dto(s) for s in snapshots]
            earliest = min((s.recorded_at for s in snapshots), default=None)
            latest = max((s.recorded_at for s in snapshots), default=None)

            return KPIHistoryDTO(
                kpi=kpi_to_dto(kpi),
                snapshots=snapshot_dtos,
                count=len(snapshot_dtos),
                earliest_at=earliest,
                latest_at=latest,
            )