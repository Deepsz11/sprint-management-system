"""List business outcomes use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.mappers import outcome_to_dto
from app.application.use_cases.base import UseCase
from app.domain.repositories.specifications import OutcomeFilter, PageRequest
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListBusinessOutcomesQuery:
    """Filter + pagination query for business outcomes."""

    context: RequestContext
    page: PageDTO = field(default_factory=PageDTO)
    owner_id: UUID | None = None
    statuses: tuple[str, ...] = ()
    target_before: date | None = None
    target_after: date | None = None
    search: str | None = None


class ListBusinessOutcomesUseCase(
    UseCase[ListBusinessOutcomesQuery, PaginatedResultDTO[BusinessOutcomeDTO]]
):
    """List business outcomes for the caller's organization."""

    def execute(
        self, query: ListBusinessOutcomesQuery
    ) -> PaginatedResultDTO[BusinessOutcomeDTO]:
        PermissionRegistry.ensure(query.context.actor, Permission.OUTCOME_READ)

        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )
        spec = OutcomeFilter(
            organization_id=query.context.organization_id,
            owner_id=query.owner_id,
            statuses=query.statuses,
            target_before=query.target_before,
            target_after=query.target_after,
            search=query.search,
        )

        with self._uow_factory() as uow:
            items = uow.outcomes.find(spec, page)
            total = uow.outcomes.count(spec)

        return PaginatedResultDTO[BusinessOutcomeDTO](
            items=[outcome_to_dto(o) for o in items],
            total=total,
            limit=page.limit,
            offset=page.offset,
        )