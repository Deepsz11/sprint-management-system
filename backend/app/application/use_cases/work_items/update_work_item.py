"""Update work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.entities.work_item_extensions import (
    apply_status_change,
    normalize_labels,
)
from app.domain.enums import WorkItemPriority, WorkItemStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateWorkItemCommand:
    """Partial update command for a work item."""

    work_item_id: UUID
    context: RequestContext
    title: str | None = None
    description: str | None = None
    priority: WorkItemPriority | None = None
    status: WorkItemStatus | None = None
    story_points: int | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    assignee_id: UUID | None = None
    labels: list[str] | None = None
    _sprint_id_provided: bool = False
    _parent_id_provided: bool = False
    _epic_id_provided: bool = False
    _assignee_id_provided: bool = False


class UpdateWorkItemUseCase(UseCase[UpdateWorkItemCommand, WorkItemDTO]):
    """Apply a partial update to a work item."""

    def execute(self, command: UpdateWorkItemCommand) -> WorkItemDTO:
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
            org_id = project.organization_id

            if command.title is not None:
                if not command.title.strip():
                    raise ValidationError("Title cannot be empty")
                item.title = command.title.strip()
            if command.description is not None:
                item.description = command.description
            if command.priority is not None:
                item.priority = command.priority
            if command.story_points is not None:
                if command.story_points < 0:
                    raise ValidationError("Story points cannot be negative")
                item.story_points = command.story_points
            if command.estimated_hours is not None:
                if command.estimated_hours < 0:
                    raise ValidationError("Estimated hours cannot be negative")
                item.estimated_hours = command.estimated_hours
            if command.actual_hours is not None:
                if command.actual_hours < 0:
                    raise ValidationError("Actual hours cannot be negative")
                item.actual_hours = command.actual_hours
            if command.labels is not None:
                item.labels = normalize_labels(command.labels)

            if command._sprint_id_provided:
                validator.ensure_sprint_belongs_to_project(
                    command.sprint_id, item.project_id
                )
                item.sprint_id = command.sprint_id
            if command._parent_id_provided:
                validator.ensure_parent_valid(
                    command.parent_id, item.project_id, item.item_type
                )
                item.parent_id = command.parent_id
            if command._epic_id_provided:
                validator.ensure_epic_valid(
                    command.epic_id, item.project_id, item.item_type
                )
                item.epic_id = command.epic_id
            if command._assignee_id_provided:
                validator.ensure_assignee_in_org(command.assignee_id, org_id)
                item.assignee_id = command.assignee_id

            item.touch()

            if command.status is not None and command.status != item.status:
                apply_status_change(item, command.status)

            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)