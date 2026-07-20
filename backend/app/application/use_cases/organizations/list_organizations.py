"""List organizations use case."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.organization import OrganizationDTO
from app.application.mappers import organization_to_dto
from app.application.use_cases.base import UseCase
from app.domain.enums import UserRole
from app.domain.repositories.specifications import PageRequest


@dataclass(frozen=True)
class ListOrganizationsQuery:
    """Query for listing organizations."""

    page: PageDTO
    context: RequestContext


class ListOrganizationsUseCase(
    UseCase[ListOrganizationsQuery, PaginatedResultDTO[OrganizationDTO]]
):
    """List organizations visible to the actor."""

    def execute(
        self, query: ListOrganizationsQuery
    ) -> PaginatedResultDTO[OrganizationDTO]:
        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )

        with self._uow_factory() as uow:
            if query.context.actor.role == UserRole.SUPER_ADMIN:
                items = uow.organizations.list_all(page)
                total = uow.organizations.count()
            elif query.context.actor.organization_id is not None:
                org = uow.organizations.get_by_id(query.context.actor.organization_id)
                items = [org] if org is not None else []
                total = 1 if org is not None else 0
            else:
                items = []
                total = 0

            return PaginatedResultDTO[OrganizationDTO](
                items=[organization_to_dto(o) for o in items],
                total=total,
                limit=page.limit,
                offset=page.offset,
            )