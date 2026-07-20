"""Move work item to a sprint (or backlog)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.enums import WorkItemStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class MoveWorkItemToSprintCommand:
    """Move a work item to a sprint or back to the backlog."""

    work_item_id: UUID
    sprint_id: UUID | None
    context: RequestContext


class MoveWorkItemToSprintUseCase(
    UseCase[MoveWorkItemToSprintCommand, WorkItemDTO]
):
    """Move a work item to a target sprint (or unassign it from any sprint)."""

    def execute(self, command: MoveWorkItemToSprintCommand) -> WorkItemDTO:
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

            if item.status == WorkItemStatus.DONE:
                raise BusinessRuleViolationError(
                    "Cannot move a completed work item between sprints"
                )

            validator = WorkItemValidator(uow)
            validator.ensure_sprint_belongs_to_project(
                command.sprint_id, item.project_id
            )

            if command.sprint_id is None:
                item.remove_from_sprint()
            else:
                item.assign_to_sprint(command.sprint_id)

            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)