"""Update KPI target value use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError, ValidationError
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.kpi_extensions import (
    KPILifecycle,
    ensure_target_direction_consistent,
)
from app.domain.enums import AuditAction
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateKPITargetCommand:
    """Update a KPI's target value and record the change."""

    kpi_id: UUID
    target_value: Decimal
    context: RequestContext
    reason: str | None = None


class UpdateKPITargetUseCase(UseCase[UpdateKPITargetCommand, KPIDTO]):
    """Update the target of a KPI while auditing the change."""

    def execute(self, command: UpdateKPITargetCommand) -> KPIDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )
            KPILifecycle.ensure_editable(kpi)

            if not kpi.is_active:
                raise BusinessRuleViolationError(
                    "Cannot change target for an inactive KPI"
                )
            if kpi.target_value == command.target_value:
                raise ValidationError(
                    "New target value must differ from the current target"
                )

            ensure_target_direction_consistent(
                kpi.baseline_value, command.target_value, kpi.direction.value
            )

            previous = kpi.target_value
            kpi.target_value = command.target_value
            kpi.touch()
            updated = uow.kpis.update(kpi)

            audit_entry = AuditLog(
                organization_id=kpi.organization_id,
                actor_id=command.context.actor_id,
                action=AuditAction.UPDATE,
                resource_type="kpi.target",
                resource_id=kpi.id,
                ip_address=command.context.ip_address,
                user_agent=command.context.user_agent,
                changes={
                    "previous_target": str(previous) if previous is not None else None,
                    "new_target": str(command.target_value),
                },
                metadata={
                    "reason": command.reason or "",
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            uow.audit_logs.add(audit_entry)

            uow.commit()
            return kpi_to_dto(updated)