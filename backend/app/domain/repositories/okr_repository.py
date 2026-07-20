"""Repository contracts for Objective and KeyResult aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.okr import KeyResult, Objective
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class ObjectiveRepositoryContract(Repository[Objective], ABC):
    """Repository contract for the Objective aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return objectives for an organization."""

    @abstractmethod
    def list_by_team(
        self, team_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return objectives for a team."""

    @abstractmethod
    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return objectives owned by a user."""

    @abstractmethod
    def list_by_parent(self, parent_id: UUID) -> Sequence[Objective]:
        """Return objectives that cascade from a parent objective."""

    @abstractmethod
    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return active objectives for an organization."""

    @abstractmethod
    def count_by_organization(self, organization_id: UUID) -> int:
        """Return the number of objectives in an organization."""


class KeyResultRepositoryContract(Repository[KeyResult], ABC):
    """Repository contract for the KeyResult aggregate."""

    @abstractmethod
    def list_by_objective(self, objective_id: UUID) -> Sequence[KeyResult]:
        """Return key results attached to an objective."""

    @abstractmethod
    def list_by_kpi(self, kpi_id: UUID) -> Sequence[KeyResult]:
        """Return key results linked to a KPI."""

    @abstractmethod
    def count_by_objective(self, objective_id: UUID) -> int:
        """Return the number of key results on an objective."""

    @abstractmethod
    def delete_by_objective(self, objective_id: UUID) -> int:
        """Soft-delete all key results for an objective. Returns count deleted."""