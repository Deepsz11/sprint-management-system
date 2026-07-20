"""Assign work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class AssignWorkItemCommand:
    """Assign or unassign a work item."""

    work_item_id: UUID
    assignee_id: UUID | None
    context: RequestContext


class AssignWorkItemUseCase(UseCase[AssignWorkItemCommand, WorkItemDTO]):
    """Reassign a work item to a user (or unassign)."""

    def execute(self, command: AssignWorkItemCommand) -> WorkItemDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(command.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {command.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id
            )

            validator = WorkItemValidator(uow)
            validator.ensure_assignee_in_org(
                command.assignee_id, project.organization_id
            )

            item.reassign(command.assignee_id)
            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)