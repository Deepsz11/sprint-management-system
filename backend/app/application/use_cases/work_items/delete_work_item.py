"""Delete work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.enums import WorkItemStatus, WorkItemType
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class DeleteWorkItemCommand:
    """Delete (soft) a work item."""

    work_item_id: UUID
    context: RequestContext


class DeleteWorkItemUseCase(UseCase[DeleteWorkItemCommand, None]):
    """Soft-delete a work item after checking business rules."""

    def execute(self, command: DeleteWorkItemCommand) -> None:
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
                    "Completed work items cannot be deleted; cancel them instead"
                )

            if item.item_type == WorkItemType.EPIC:
                children = uow.work_items.list_by_epic(item.id)
                if children:
                    raise BusinessRuleViolationError(
                        "Cannot delete an epic that still has child work items"
                    )

            uow.work_items.delete(command.work_item_id)
            uow.commit()