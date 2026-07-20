"""Repository contracts for User and TeamMembership aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.user import TeamMembership, User
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class UserRepositoryContract(Repository[User], ABC):
    """Repository contract for the User aggregate."""

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Return a user by email (case-insensitive)."""

    @abstractmethod
    def email_exists(self, email: str, exclude_id: UUID | None = None) -> bool:
        """Return True when the email is already in use."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[User]:
        """Return users belonging to an organization."""

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[User]:
        """Return users who are members of a team."""

    @abstractmethod
    def list_by_role(
        self, organization_id: UUID, role: str, page: PageRequest
    ) -> Sequence[User]:
        """Return users of a given role in an organization."""

    @abstractmethod
    def search(
        self, organization_id: UUID, query: str, page: PageRequest
    ) -> Sequence[User]:
        """Search users within an organization."""

    @abstractmethod
    def count_by_organization(self, organization_id: UUID) -> int:
        """Return total user count for an organization."""


class TeamMembershipRepositoryContract(Repository[TeamMembership], ABC):
    """Repository contract for TeamMembership associations."""

    @abstractmethod
    def get_by_team_and_user(
        self, team_id: UUID, user_id: UUID
    ) -> TeamMembership | None:
        """Return a membership by team and user."""

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[TeamMembership]:
        """Return all memberships in a team."""

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> Sequence[TeamMembership]:
        """Return all memberships for a user."""

    @abstractmethod
    def remove_by_team_and_user(self, team_id: UUID, user_id: UUID) -> None:
        """Remove a user's membership from a team."""