"""Delete KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.use_cases.base import UseCase
from app.application.validators.kpi_validator import KPIValidator
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class DeleteKPICommand:
    """Soft-delete a KPI."""

    kpi_id: UUID
    context: RequestContext


class DeleteKPIUseCase(UseCase[DeleteKPICommand, None]):
    """Soft-delete a KPI after enforcing business rules."""

    def execute(self, command: DeleteKPICommand) -> None:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )

            KPIValidator(uow).ensure_deletable(kpi.id)

            # Detach from any key results that reference this KPI so those
            # remain valid at the objective level.
            for key_result in uow.key_results.list_by_kpi(kpi.id):
                key_result.kpi_id = None
                key_result.touch()
                uow.key_results.update(key_result)

            uow.kpis.delete(command.kpi_id)
            uow.commit()