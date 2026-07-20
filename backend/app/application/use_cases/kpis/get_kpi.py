"""Get KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class GetKPIQuery:
    """Query for a single KPI."""

    kpi_id: UUID
    context: RequestContext


class GetKPIUseCase(UseCase[GetKPIQuery, KPIDTO]):
    """Retrieve a KPI by ID."""

    def execute(self, query: GetKPIQuery) -> KPIDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.KPI_READ)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(query.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {query.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, kpi.organization_id
            )
            return kpi_to_dto(kpi)