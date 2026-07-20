"""Repository contract for the WorkItem aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.work_item import WorkItem
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest, WorkItemFilter


class WorkItemRepositoryContract(Repository[WorkItem], ABC):
    """Repository contract for the WorkItem aggregate."""

    @abstractmethod
    def get_by_external_key(
        self, project_id: UUID, external_key: str
    ) -> WorkItem | None:
        """Return a work item by external key within a project."""

    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[WorkItem]:
        """Return work items assigned to a sprint."""

    @abstractmethod
    def list_by_project(
        self, project_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        """Return work items in a project."""

    @abstractmethod
    def list_by_epic(self, epic_id: UUID) -> Sequence[WorkItem]:
        """Return child work items of an epic."""

    @abstractmethod
    def list_by_parent(self, parent_id: UUID) -> Sequence[WorkItem]:
        """Return child work items of a parent."""

    @abstractmethod
    def list_by_assignee(
        self, user_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        """Return work items assigned to a user."""

    @abstractmethod
    def list_unattributed(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        """Return completed work items lacking outcome attributions."""

    @abstractmethod
    def find(self, spec: WorkItemFilter, page: PageRequest) -> Sequence[WorkItem]:
        """Return work items matching a filter specification."""

    @abstractmethod
    def count(self, spec: WorkItemFilter) -> int:
        """Return count of work items matching a filter."""

    @abstractmethod
    def bulk_reassign_sprint(
        self, work_item_ids: Sequence[UUID], sprint_id: UUID | None
    ) -> int:
        """Reassign multiple work items to a sprint (or unassign). Returns count updated."""