"""Cross-aggregate validators for work item operations."""

from __future__ import annotations

from uuid import UUID

from app.core.exceptions import NotFoundError, ValidationError
from app.domain.entities.user import User
from app.domain.enums import WorkItemType
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class WorkItemValidator:
    """Validates references between work items, projects, sprints, and users."""

    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self._uow = uow

    def ensure_project_belongs_to_org(
        self, project_id: UUID, organization_id: UUID | None
    ) -> None:
        project = self._uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        if organization_id is not None and project.organization_id != organization_id:
            raise ValidationError("Project does not belong to your organization")

    def ensure_sprint_belongs_to_project(
        self, sprint_id: UUID | None, project_id: UUID
    ) -> None:
        if sprint_id is None:
            return
        sprint = self._uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        if sprint.project_id != project_id:
            raise ValidationError("Sprint does not belong to the given project")

    def ensure_assignee_in_org(
        self, assignee_id: UUID | None, organization_id: UUID | None
    ) -> User | None:
        if assignee_id is None:
            return None
        user = self._uow.users.get_by_id(assignee_id)
        if user is None:
            raise NotFoundError(f"User {assignee_id} not found")
        if not user.is_active:
            raise ValidationError("Assignee is not an active user")
        if organization_id is not None and user.organization_id != organization_id:
            raise ValidationError("Assignee does not belong to your organization")
        return user

    def ensure_parent_valid(
        self,
        parent_id: UUID | None,
        project_id: UUID,
        item_type: WorkItemType,
    ) -> None:
        if parent_id is None:
            return
        parent = self._uow.work_items.get_by_id(parent_id)
        if parent is None:
            raise NotFoundError(f"Parent work item {parent_id} not found")
        if parent.project_id != project_id:
            raise ValidationError(
                "Parent work item must belong to the same project"
            )
        if item_type == WorkItemType.EPIC and parent.item_type == WorkItemType.EPIC:
            raise ValidationError("Epics cannot have another epic as parent")

    def ensure_epic_valid(
        self,
        epic_id: UUID | None,
        project_id: UUID,
        item_type: WorkItemType,
    ) -> None:
        if epic_id is None:
            return
        if item_type == WorkItemType.EPIC:
            raise ValidationError("An epic cannot belong to another epic")
        epic = self._uow.work_items.get_by_id(epic_id)
        if epic is None:
            raise NotFoundError(f"Epic {epic_id} not found")
        if epic.item_type != WorkItemType.EPIC:
            raise ValidationError("Referenced item is not an epic")
        if epic.project_id != project_id:
            raise ValidationError("Epic must belong to the same project")