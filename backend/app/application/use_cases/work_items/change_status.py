"""Change work item status use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.entities.work_item_extensions import apply_status_change
from app.domain.enums import WorkItemStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ChangeWorkItemStatusCommand:
    """Change the status of a work item."""

    work_item_id: UUID
    target_status: WorkItemStatus
    context: RequestContext
    actual_hours: float | None = None


class ChangeWorkItemStatusUseCase(
    UseCase[ChangeWorkItemStatusCommand, WorkItemDTO]
):
    """Apply a validated status transition to a work item."""

    def execute(self, command: ChangeWorkItemStatusCommand) -> WorkItemDTO:
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

            if (
                command.target_status == WorkItemStatus.DONE
                and command.actual_hours is not None
            ):
                if command.actual_hours < 0:
                    raise ValidationError("Actual hours cannot be negative")
                item.actual_hours = command.actual_hours

            apply_status_change(item, command.target_status)
            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)