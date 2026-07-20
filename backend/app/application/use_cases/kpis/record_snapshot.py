"""Record KPI snapshot use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import MetricSnapshotDTO
from app.application.mappers import metric_snapshot_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError, ValidationError
from app.domain.entities.kpi import MetricSnapshot
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class RecordKPISnapshotCommand:
    """Command to record a KPI metric snapshot."""

    kpi_id: UUID
    value: Decimal
    context: RequestContext
    recorded_at: datetime | None = None
    source: str | None = None
    notes: str | None = None
    context_metadata: dict[str, str] = field(default_factory=dict)


class RecordKPISnapshotUseCase(
    UseCase[RecordKPISnapshotCommand, MetricSnapshotDTO]
):
    """Record a new metric snapshot for a KPI and update its current value."""

    def execute(
        self, command: RecordKPISnapshotCommand
    ) -> MetricSnapshotDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )

            if not kpi.is_active:
                raise BusinessRuleViolationError(
                    "Cannot record snapshots for an inactive KPI"
                )

            recorded_at = command.recorded_at or datetime.now(timezone.utc)
            if recorded_at.tzinfo is None:
                recorded_at = recorded_at.replace(tzinfo=timezone.utc)
            if recorded_at > datetime.now(timezone.utc):
                raise ValidationError("Snapshot recorded_at cannot be in the future")

            snapshot = MetricSnapshot(
                kpi_id=kpi.id,
                value=command.value,
                recorded_at=recorded_at,
                source=command.source,
                notes=command.notes,
                context=dict(command.context_metadata),
            )
            created = uow.metric_snapshots.add(snapshot)

            latest = uow.metric_snapshots.latest_for_kpi(kpi.id)
            if latest is None or latest.recorded_at <= created.recorded_at:
                kpi.record_current_value(command.value)
                uow.kpis.update(kpi)

            uow.commit()
            return metric_snapshot_to_dto(created)