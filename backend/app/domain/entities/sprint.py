"""Sprint entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import SprintStatus
from app.domain.value_objects import DateRange


@dataclass
class Sprint(SoftDeletableEntity):
    """A time-boxed sprint containing work items."""

    project_id: UUID = field(default_factory=lambda: UUID(int=0))
    name: str = ""
    goal: str | None = None
    start_date: date = field(default_factory=date.today)
    end_date: date = field(default_factory=date.today)
    status: SprintStatus = SprintStatus.PLANNED
    started_at: datetime | None = None
    completed_at: datetime | None = None
    planned_capacity: int = 0
    completed_points: int = 0

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Sprint name is required")
        if self.end_date < self.start_date:
            raise ValidationError("Sprint end date cannot be before start date")
        if self.planned_capacity < 0:
            raise ValidationError("Planned capacity cannot be negative")

    @property
    def date_range(self) -> DateRange:
        return DateRange(self.start_date, self.end_date)

    @property
    def is_active(self) -> bool:
        return self.status == SprintStatus.ACTIVE

    def start(self) -> None:
        if self.status != SprintStatus.PLANNED:
            raise BusinessRuleViolationError(
                f"Cannot start sprint from status {self.status.value}"
            )
        self.status = SprintStatus.ACTIVE
        self.started_at = datetime.now(timezone.utc)
        self.touch()

    def complete(self, completed_points: int) -> None:
        if self.status != SprintStatus.ACTIVE:
            raise BusinessRuleViolationError(
                f"Cannot complete sprint from status {self.status.value}"
            )
        if completed_points < 0:
            raise ValidationError("Completed points cannot be negative")
        self.status = SprintStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.completed_points = completed_points
        self.touch()

    def cancel(self) -> None:
        if self.status == SprintStatus.COMPLETED:
            raise BusinessRuleViolationError("Cannot cancel a completed sprint")
        self.status = SprintStatus.CANCELLED
        self.touch()

    @property
    def completion_rate(self) -> float:
        if self.planned_capacity == 0:
            return 0.0
        return round(self.completed_points / self.planned_capacity, 4)