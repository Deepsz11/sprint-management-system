"""Repository contract for the Project aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.project import Project
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class ProjectRepositoryContract(Repository[Project], ABC):
    """Repository contract for the Project aggregate."""

    @abstractmethod
    def get_by_key(self, organization_id: UUID, key: str) -> Project | None:
        """Return a project by its unique key within an organization."""

    @abstractmethod
    def get_by_slug(self, organization_id: UUID, slug: str) -> Project | None:
        """Return a project by its slug within an organization."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        """Return projects in an organization."""

    @abstractmethod
    def list_by_team(
        self, team_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        """Return projects for a specific team."""

    @abstractmethod
    def key_exists(
        self, organization_id: UUID, key: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when a project key is already in use."""

    @abstractmethod
    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when a project slug is already in use."""

    @abstractmethod
    def count_by_organization(
        self, organization_id: UUID, include_archived: bool = False
    ) -> int:
        """Return project count for an organization."""