"""Repository contract for the Sprint aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Sequence
from uuid import UUID

from app.domain.entities.sprint import Sprint
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest, SprintFilter


class SprintRepositoryContract(Repository[Sprint], ABC):
    """Repository contract for the Sprint aggregate."""

    @abstractmethod
    def list_by_project(
        self, project_id: UUID, page: PageRequest
    ) -> Sequence[Sprint]:
        """Return sprints for a project."""

    @abstractmethod
    def get_active_for_project(self, project_id: UUID) -> Sprint | None:
        """Return the currently active sprint for a project, if any."""

    @abstractmethod
    def list_completed_in_range(
        self, organization_id: UUID, start: date, end: date
    ) -> Sequence[Sprint]:
        """Return sprints completed within a date range for an organization."""

    @abstractmethod
    def list_active_for_organization(
        self, organization_id: UUID
    ) -> Sequence[Sprint]:
        """Return all currently active sprints across an organization."""

    @abstractmethod
    def find(self, spec: SprintFilter, page: PageRequest) -> Sequence[Sprint]:
        """Return sprints matching a filter specification."""

    @abstractmethod
    def count(self, spec: SprintFilter) -> int:
        """Return the count of sprints matching a filter specification."""

    @abstractmethod
    def latest_by_project(self, project_id: UUID, limit: int = 5) -> Sequence[Sprint]:
        """Return the most recent sprints in a project."""