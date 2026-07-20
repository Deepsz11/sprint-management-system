"""Repository contract for the BusinessOutcome aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import OutcomeFilter, PageRequest


class BusinessOutcomeRepositoryContract(Repository[BusinessOutcome], ABC):
    """Repository contract for the BusinessOutcome aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes for an organization."""

    @abstractmethod
    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes owned by a user."""

    @abstractmethod
    def list_off_track(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        """Return outcomes flagged as off track."""

    @abstractmethod
    def list_at_risk(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        """Return outcomes flagged as at risk."""

    @abstractmethod
    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes with active status."""

    @abstractmethod
    def find(
        self, spec: OutcomeFilter, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes matching a filter specification."""

    @abstractmethod
    def count(self, spec: OutcomeFilter) -> int:
        """Return count of outcomes matching a filter."""

    @abstractmethod
    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when an outcome with the given name exists in the organization."""