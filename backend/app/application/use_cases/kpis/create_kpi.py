"""Create KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.kpi_validator import KPIValidator
from app.core.exceptions import ConflictError
from app.domain.entities.kpi import KPI
from app.domain.entities.kpi_extensions import (
    ensure_currency_matches_unit,
    ensure_target_direction_consistent,
)
from app.domain.enums import KPIDirection, KPIUnit
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class CreateKPICommand:
    """Create KPI command."""

    name: str
    context: RequestContext
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    description: str | None = None
    unit: KPIUnit = KPIUnit.COUNT
    currency: str | None = None
    direction: KPIDirection = KPIDirection.INCREASE
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = None
    refresh_frequency_hours: int | None = None


class CreateKPIUseCase(UseCase[CreateKPICommand, KPIDTO]):
    """Create a KPI scoped to the caller's organization."""

    def execute(self, command: CreateKPICommand) -> KPIDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        org_id = command.context.organization_id
        if org_id is None:
            raise ConflictError(
                "KPIs can only be created within an organization context"
            )

        ensure_currency_matches_unit(command.unit.value, command.currency)
        ensure_target_direction_consistent(
            command.baseline_value, command.target_value, command.direction.value
        )

        with self._uow_factory() as uow:
            validator = KPIValidator(uow)
            validator.ensure_unique_name(org_id, command.name)
            validator.ensure_owner_in_org(command.owner_id, org_id)
            validator.ensure_outcome_in_org(command.outcome_id, org_id)

            kpi = KPI(
                organization_id=org_id,
                outcome_id=command.outcome_id,
                owner_id=command.owner_id,
                name=command.name.strip(),
                description=command.description,
                unit=command.unit,
                currency=command.currency,
                direction=command.direction,
                baseline_value=command.baseline_value,
                target_value=command.target_value,
                current_value=command.current_value,
                data_source=command.data_source,
                refresh_frequency_hours=command.refresh_frequency_hours,
                is_active=True,
            )
            created = uow.kpis.add(kpi)
            uow.commit()
            return kpi_to_dto(created)