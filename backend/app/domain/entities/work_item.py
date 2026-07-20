"""Work item entity - stories, tasks, bugs, epics, spikes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType


@dataclass
class WorkItem(SoftDeletableEntity):
    """A unit of engineering work traceable to business outcomes."""

    project_id: UUID = field(default_factory=lambda: UUID(int=0))
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    external_key: str | None = None
    title: str = ""
    description: str | None = None
    item_type: WorkItemType = WorkItemType.STORY
    status: WorkItemStatus = WorkItemStatus.BACKLOG
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    story_points: int | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    labels: list[str] = field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Work item title is required")
        if len(self.title) > 500:
            raise ValidationError("Work item title must be 500 characters or fewer")
        if self.story_points is not None and self.story_points < 0:
            raise ValidationError("Story points cannot be negative")
        if self.estimated_hours is not None and self.estimated_hours < 0:
            raise ValidationError("Estimated hours cannot be negative")
        if self.actual_hours is not None and self.actual_hours < 0:
            raise ValidationError("Actual hours cannot be negative")
        if self.item_type == WorkItemType.EPIC and self.epic_id is not None:
            raise ValidationError("An epic cannot belong to another epic")
        if self.parent_id is not None and self.parent_id == self.id:
            raise ValidationError("Work item cannot be its own parent")

    @property
    def is_completed(self) -> bool:
        return self.status == WorkItemStatus.DONE

    @property
    def is_in_flight(self) -> bool:
        return self.status in {WorkItemStatus.IN_PROGRESS, WorkItemStatus.IN_REVIEW}

    def assign_to_sprint(self, sprint_id: UUID) -> None:
        if self.is_completed:
            raise BusinessRuleViolationError("Cannot reassign a completed work item")
        self.sprint_id = sprint_id
        self.touch()

    def remove_from_sprint(self) -> None:
        if self.is_completed:
            raise BusinessRuleViolationError("Cannot remove a completed work item from sprint")
        self.sprint_id = None
        self.touch()

    def start(self) -> None:
        if self.status not in {WorkItemStatus.BACKLOG, WorkItemStatus.TODO}:
            raise BusinessRuleViolationError(
                f"Cannot start work item from status {self.status.value}"
            )
        self.status = WorkItemStatus.IN_PROGRESS
        self.started_at = datetime.now(timezone.utc)
        self.touch()

    def send_for_review(self) -> None:
        if self.status != WorkItemStatus.IN_PROGRESS:
            raise BusinessRuleViolationError(
                "Work item must be in progress to be sent for review"
            )
        self.status = WorkItemStatus.IN_REVIEW
        self.touch()

    def complete(self, actual_hours: float | None = None) -> None:
        if self.status in {WorkItemStatus.DONE, WorkItemStatus.CANCELLED}:
            raise BusinessRuleViolationError(
                f"Cannot complete work item from status {self.status.value}"
            )
        if actual_hours is not None:
            if actual_hours < 0:
                raise ValidationError("Actual hours cannot be negative")
            self.actual_hours = actual_hours
        self.status = WorkItemStatus.DONE
        self.completed_at = datetime.now(timezone.utc)
        self.touch()

    def cancel(self) -> None:
        if self.status == WorkItemStatus.DONE:
            raise BusinessRuleViolationError("Cannot cancel a completed work item")
        self.status = WorkItemStatus.CANCELLED
        self.touch()

    def reassign(self, user_id: UUID | None) -> None:
        self.assignee_id = user_id
        self.touch()

    def add_label(self, label: str) -> None:
        normalized = label.strip().lower()
        if not normalized:
            raise ValidationError("Label cannot be empty")
        if normalized not in self.labels:
            self.labels.append(normalized)
            self.touch()

    def remove_label(self, label: str) -> None:
        normalized = label.strip().lower()
        if normalized in self.labels:
            self.labels.remove(normalized)
            self.touch()