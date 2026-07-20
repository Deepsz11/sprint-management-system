"""List work items use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.domain.repositories.specifications import PageRequest, WorkItemFilter
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListWorkItemsQuery:
    """Filter + pagination query for work items."""

    context: RequestContext
    page: PageDTO = field(default_factory=PageDTO)
    project_id: UUID | None = None
    sprint_id: UUID | None = None
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    epic_id: UUID | None = None
    item_types: tuple[str, ...] = ()
    statuses: tuple[str, ...] = ()
    priorities: tuple[str, ...] = ()
    labels: tuple[str, ...] = ()
    search: str | None = None
    completed_after: datetime | None = None
    completed_before: datetime | None = None


class ListWorkItemsUseCase(
    UseCase[ListWorkItemsQuery, PaginatedResultDTO[WorkItemDTO]]
):
    """List work items belonging to the caller's organization."""

    def execute(
        self, query: ListWorkItemsQuery
    ) -> PaginatedResultDTO[WorkItemDTO]:
        PermissionRegistry.ensure(query.context.actor, Permission.WORK_ITEM_READ)

        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )
        spec = WorkItemFilter(
            organization_id=query.context.organization_id,
            project_id=query.project_id,
            sprint_id=query.sprint_id,
            assignee_id=query.assignee_id,
            reporter_id=query.reporter_id,
            epic_id=query.epic_id,
            item_types=query.item_types,
            statuses=query.statuses,
            priorities=query.priorities,
            labels=query.labels,
            search=query.search,
            completed_after=query.completed_after,
            completed_before=query.completed_before,
        )

        with self._uow_factory() as uow:
            items = uow.work_items.find(spec, page)
            total = uow.work_items.count(spec)

        return PaginatedResultDTO[WorkItemDTO](
            items=[work_item_to_dto(i) for i in items],
            total=total,
            limit=page.limit,
            offset=page.offset,
        )