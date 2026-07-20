"""Query specifications used by repositories."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID


@dataclass(frozen=True)
class PageRequest:
    """Pagination request."""

    limit: int = 20
    offset: int = 0
    order_by: str = "created_at"
    descending: bool = True

    def __post_init__(self) -> None:
        if self.limit <= 0 or self.limit > 500:
            raise ValueError("limit must be between 1 and 500")
        if self.offset < 0:
            raise ValueError("offset cannot be negative")


@dataclass(frozen=True)
class WorkItemFilter:
    """Filter criteria for querying work items."""

    organization_id: UUID | None = None
    project_id: UUID | None = None
    sprint_id: UUID | None = None
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    epic_id: UUID | None = None
    item_types: tuple[str, ...] = field(default_factory=tuple)
    statuses: tuple[str, ...] = field(default_factory=tuple)
    priorities: tuple[str, ...] = field(default_factory=tuple)
    labels: tuple[str, ...] = field(default_factory=tuple)
    search: str | None = None
    completed_after: datetime | None = None
    completed_before: datetime | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class SprintFilter:
    """Filter criteria for querying sprints."""

    organization_id: UUID | None = None
    project_id: UUID | None = None
    statuses: tuple[str, ...] = field(default_factory=tuple)
    starts_after: date | None = None
    ends_before: date | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class OutcomeFilter:
    """Filter criteria for querying business outcomes."""

    organization_id: UUID | None = None
    owner_id: UUID | None = None
    statuses: tuple[str, ...] = field(default_factory=tuple)
    target_before: date | None = None
    target_after: date | None = None
    search: str | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class KPIFilter:
    """Filter criteria for querying KPIs."""

    organization_id: UUID | None = None
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    units: tuple[str, ...] = field(default_factory=tuple)
    is_active: bool | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class AttributionFilter:
    """Filter criteria for querying attributions."""

    organization_id: UUID | None = None
    work_item_id: UUID | None = None
    sprint_id: UUID | None = None
    outcome_id: UUID | None = None
    kpi_id: UUID | None = None
    key_result_id: UUID | None = None
    strengths: tuple[str, ...] = field(default_factory=tuple)
    methods: tuple[str, ...] = field(default_factory=tuple)
    include_deleted: bool = False


@dataclass(frozen=True)
class AuditLogFilter:
    """Filter criteria for querying audit logs."""

    organization_id: UUID | None = None
    actor_id: UUID | None = None
    resource_type: str | None = None
    resource_id: UUID | None = None
    actions: tuple[str, ...] = field(default_factory=tuple)
    occurred_after: datetime | None = None
    occurred_before: datetime | None = None


@dataclass(frozen=True)
class MetricSnapshotFilter:
    """Filter criteria for querying metric snapshots."""

    kpi_id: UUID | None = None
    recorded_after: datetime | None = None
    recorded_before: datetime | None = None
    source: str | None = None


@dataclass(frozen=True)
class NotificationFilter:
    """Filter criteria for querying notifications."""

    recipient_id: UUID | None = None
    organization_id: UUID | None = None
    statuses: tuple[str, ...] = field(default_factory=tuple)
    channels: tuple[str, ...] = field(default_factory=tuple)
    event_types: tuple[str, ...] = field(default_factory=tuple)