"""Repository contracts for Organization and Team aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.organization import Organization, Team
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class OrganizationRepositoryContract(Repository[Organization], ABC):
    """Repository contract for the Organization aggregate."""

    @abstractmethod
    def get_by_slug(self, slug: str) -> Organization | None:
        """Return an organization by its unique slug."""

    @abstractmethod
    def get_by_billing_email(self, email: str) -> Organization | None:
        """Return an organization by its billing email."""

    @abstractmethod
    def list_all(self, page: PageRequest) -> Sequence[Organization]:
        """Return a paginated list of organizations."""

    @abstractmethod
    def list_active(self, page: PageRequest) -> Sequence[Organization]:
        """Return active organizations."""

    @abstractmethod
    def count(self) -> int:
        """Return total organization count."""

    @abstractmethod
    def slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        """Return True when the slug is already in use."""


class TeamRepositoryContract(Repository[Team], ABC):
    """Repository contract for the Team aggregate."""

    @abstractmethod
    def get_by_slug(self, organization_id: UUID, slug: str) -> Team | None:
        """Return a team by organization and slug."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Team]:
        """Return teams in an organization."""

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> Sequence[Team]:
        """Return teams that a user belongs to."""

    @abstractmethod
    def count_by_organization(self, organization_id: UUID) -> int:
        """Return the count of teams in an organization."""

    @abstractmethod
    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when the slug is already in use in this organization."""