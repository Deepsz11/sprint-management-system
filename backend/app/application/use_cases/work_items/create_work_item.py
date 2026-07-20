"""Create work item use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import ConflictError
from app.domain.entities.work_item import WorkItem
from app.domain.entities.work_item_extensions import (
    ensure_hierarchy,
    normalize_labels,
)
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.domain.services.permissions import Permission, PermissionRegistry
from app.domain.services.authorization_service import AuthorizationDomainService


@dataclass(frozen=True)
class CreateWorkItemCommand:
    """Create work item command."""

    project_id: UUID
    title: str
    context: RequestContext
    description: str | None = None
    item_type: WorkItemType = WorkItemType.STORY
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    story_points: int | None = None
    estimated_hours: float | None = None
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    assignee_id: UUID | None = None
    external_key: str | None = None
    labels: list[str] = field(default_factory=list)


class CreateWorkItemUseCase(UseCase[CreateWorkItemCommand, WorkItemDTO]):
    """Create a new work item."""

    def execute(self, command: CreateWorkItemCommand) -> WorkItemDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            validator = WorkItemValidator(uow)
            org_id = command.context.organization_id

            validator.ensure_project_belongs_to_org(command.project_id, org_id)
            project = uow.projects.get_by_id(command.project_id)
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id if project else None
            )

            ensure_hierarchy(command.item_type, command.epic_id, command.parent_id)
            validator.ensure_sprint_belongs_to_project(
                command.sprint_id, command.project_id
            )
            validator.ensure_parent_valid(
                command.parent_id, command.project_id, command.item_type
            )
            validator.ensure_epic_valid(
                command.epic_id, command.project_id, command.item_type
            )
            validator.ensure_assignee_in_org(command.assignee_id, org_id)

            if command.external_key:
                existing = uow.work_items.get_by_external_key(
                    command.project_id, command.external_key
                )
                if existing is not None:
                    raise ConflictError(
                        f"External key '{command.external_key}' is already in use"
                    )

            item = WorkItem(
                project_id=command.project_id,
                sprint_id=command.sprint_id,
                parent_id=command.parent_id,
                epic_id=command.epic_id,
                external_key=command.external_key,
                title=command.title,
                description=command.description,
                item_type=command.item_type,
                status=WorkItemStatus.BACKLOG,
                priority=command.priority,
                story_points=command.story_points,
                estimated_hours=command.estimated_hours,
                assignee_id=command.assignee_id,
                reporter_id=command.context.actor_id,
                labels=normalize_labels(command.labels),
            )
            created = uow.work_items.add(item)
            uow.commit()
            return work_item_to_dto(created)