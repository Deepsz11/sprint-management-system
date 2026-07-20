"""Repository contracts for OutcomeAttribution and Evidence aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.attribution import Evidence, OutcomeAttribution
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import AttributionFilter, PageRequest


class AttributionRepositoryContract(Repository[OutcomeAttribution], ABC):
    """Repository contract for the OutcomeAttribution aggregate."""

    @abstractmethod
    def list_by_work_item(
        self, work_item_id: UUID
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions for a work item."""

    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[OutcomeAttribution]:
        """Return attributions attached to a sprint."""

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[OutcomeAttribution]:
        """Return attributions referencing a business outcome."""

    @abstractmethod
    def list_by_kpi(self, kpi_id: UUID) -> Sequence[OutcomeAttribution]:
        """Return attributions referencing a KPI."""

    @abstractmethod
    def list_by_key_result(
        self, key_result_id: UUID
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions referencing a key result."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions across an organization."""

    @abstractmethod
    def find(
        self, spec: AttributionFilter, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions matching a filter."""

    @abstractmethod
    def count(self, spec: AttributionFilter) -> int:
        """Return count of attributions matching a filter."""

    @abstractmethod
    def exists_for_pair(
        self,
        work_item_id: UUID | None,
        sprint_id: UUID | None,
        outcome_id: UUID | None,
        kpi_id: UUID | None,
        key_result_id: UUID | None,
    ) -> bool:
        """Return True when an attribution linking the given subject to target exists."""


class EvidenceRepositoryContract(Repository[Evidence], ABC):
    """Repository contract for Evidence records."""

    @abstractmethod
    def list_by_attribution(self, attribution_id: UUID) -> Sequence[Evidence]:
        """Return evidence records linked to an attribution."""

    @abstractmethod
    def count_by_attribution(self, attribution_id: UUID) -> int:
        """Return count of evidence records for an attribution."""

    @abstractmethod
    def delete_by_attribution(self, attribution_id: UUID) -> int:
        """Soft-delete all evidence for an attribution. Returns count deleted."""