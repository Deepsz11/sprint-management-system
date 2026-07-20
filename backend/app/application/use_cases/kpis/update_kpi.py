"""Update KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.kpi_validator import KPIValidator
from app.core.exceptions import NotFoundError
from app.domain.entities.kpi_extensions import (
    KPILifecycle,
    ensure_baseline_stable,
    ensure_target_direction_consistent,
)
from app.domain.enums import KPIDirection
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateKPICommand:
    """Update KPI command."""

    kpi_id: UUID
    context: RequestContext
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    direction: KPIDirection | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = None
    refresh_frequency_hours: int | None = None
    is_active: bool | None = None
    _outcome_provided: bool = False
    _owner_provided: bool = False
    _name_provided: bool = False
    _description_provided: bool = False
    _direction_provided: bool = False
    _baseline_provided: bool = False
    _target_provided: bool = False
    _current_provided: bool = False
    _data_source_provided: bool = False
    _refresh_provided: bool = False
    _is_active_provided: bool = False


class UpdateKPIUseCase(UseCase[UpdateKPICommand, KPIDTO]):
    """Update a KPI."""

    def execute(self, command: UpdateKPICommand) -> KPIDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )
            KPILifecycle.ensure_editable(kpi)

            validator = KPIValidator(uow)

            if command._name_provided and command.name is not None:
                validator.ensure_unique_name(
                    kpi.organization_id, command.name, exclude_id=kpi.id
                )
                kpi.name = command.name.strip()

            if command._description_provided:
                kpi.description = command.description

            if command._outcome_provided:
                validator.ensure_outcome_in_org(command.outcome_id, kpi.organization_id)
                kpi.outcome_id = command.outcome_id

            if command._owner_provided:
                validator.ensure_owner_in_org(command.owner_id, kpi.organization_id)
                kpi.owner_id = command.owner_id

            if command._direction_provided and command.direction is not None:
                kpi.direction = command.direction

            if command._baseline_provided:
                ensure_baseline_stable(kpi, command.baseline_value)
                kpi.baseline_value = command.baseline_value

            if command._target_provided:
                kpi.target_value = command.target_value

            if command._current_provided:
                kpi.current_value = command.current_value

            if command._data_source_provided:
                kpi.data_source = command.data_source

            if command._refresh_provided:
                kpi.refresh_frequency_hours = command.refresh_frequency_hours

            if command._is_active_provided and command.is_active is not None:
                if command.is_active:
                    kpi.activate()
                else:
                    kpi.deactivate()

            ensure_target_direction_consistent(
                kpi.baseline_value, kpi.target_value, kpi.direction.value
            )

            kpi.touch()
            updated = uow.kpis.update(kpi)
            uow.commit()
            return kpi_to_dto(updated)