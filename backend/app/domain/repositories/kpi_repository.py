"""Repository contracts for KPI and MetricSnapshot aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence
from uuid import UUID

from app.domain.entities.kpi import KPI, MetricSnapshot
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import (
    KPIFilter,
    MetricSnapshotFilter,
    PageRequest,
)


class KPIRepositoryContract(Repository[KPI], ABC):
    """Repository contract for the KPI aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[KPI]:
        """Return KPIs for an organization."""

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[KPI]:
        """Return KPIs linked to a specific business outcome."""

    @abstractmethod
    def list_by_owner(self, owner_id: UUID, page: PageRequest) -> Sequence[KPI]:
        """Return KPIs owned by a user."""

    @abstractmethod
    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[KPI]:
        """Return active KPIs in an organization."""

    @abstractmethod
    def find(self, spec: KPIFilter, page: PageRequest) -> Sequence[KPI]:
        """Return KPIs matching a filter."""

    @abstractmethod
    def count(self, spec: KPIFilter) -> int:
        """Return count of KPIs matching a filter."""

    @abstractmethod
    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when a KPI name already exists in the organization."""


class MetricSnapshotRepositoryContract(Repository[MetricSnapshot], ABC):
    """Repository contract for MetricSnapshot records."""

    @abstractmethod
    def list_by_kpi(
        self, kpi_id: UUID, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        """Return snapshots for a KPI ordered by recorded_at descending."""

    @abstractmethod
    def latest_for_kpi(self, kpi_id: UUID) -> MetricSnapshot | None:
        """Return the most recent snapshot for a KPI."""

    @abstractmethod
    def list_in_range(
        self, kpi_id: UUID, start: datetime, end: datetime
    ) -> Sequence[MetricSnapshot]:
        """Return snapshots for a KPI within an inclusive time range."""

    @abstractmethod
    def find(
        self, spec: MetricSnapshotFilter, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        """Return snapshots matching a filter."""

    @abstractmethod
    def delete_older_than(self, kpi_id: UUID, cutoff: datetime) -> int:
        """Purge snapshots older than a cutoff. Returns count purged."""