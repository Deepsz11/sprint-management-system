"""Get work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class GetWorkItemQuery:
    """Query for a single work item."""

    work_item_id: UUID
    context: RequestContext


class GetWorkItemUseCase(UseCase[GetWorkItemQuery, WorkItemDTO]):
    """Retrieve a work item by ID."""

    def execute(self, query: GetWorkItemQuery) -> WorkItemDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.WORK_ITEM_READ)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(query.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {query.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, project.organization_id
            )
            return work_item_to_dto(item)