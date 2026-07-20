"""List KPIs use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.domain.repositories.specifications import KPIFilter, PageRequest
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListKPIsQuery:
    """Filter + pagination query for KPIs."""

    context: RequestContext
    page: PageDTO = field(default_factory=PageDTO)
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    units: tuple[str, ...] = ()
    is_active: bool | None = None


class ListKPIsUseCase(UseCase[ListKPIsQuery, PaginatedResultDTO[KPIDTO]]):
    """List KPIs for the caller's organization."""

    def execute(self, query: ListKPIsQuery) -> PaginatedResultDTO[KPIDTO]:
        PermissionRegistry.ensure(query.context.actor, Permission.KPI_READ)

        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )
        spec = KPIFilter(
            organization_id=query.context.organization_id,
            outcome_id=query.outcome_id,
            owner_id=query.owner_id,
            units=query.units,
            is_active=query.is_active,
        )

        with self._uow_factory() as uow:
            items = uow.kpis.find(spec, page)
            total = uow.kpis.count(spec)

        return PaginatedResultDTO[KPIDTO](
            items=[kpi_to_dto(k) for k in items],
            total=total,
            limit=page.limit,
            offset=page.offset,
        )