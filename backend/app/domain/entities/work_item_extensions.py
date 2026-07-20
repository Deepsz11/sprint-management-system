"""Extension helpers for the WorkItem aggregate.

These helpers centralize state-transition rules and derived validation used by
Work Item use cases. Behavior lives here (not inside the raw entity file) so we
avoid touching the previously-generated `WorkItem` module.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Final

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.work_item import WorkItem
from app.domain.enums import WorkItemStatus, WorkItemType


_ALLOWED_TRANSITIONS: Final[dict[WorkItemStatus, frozenset[WorkItemStatus]]] = {
    WorkItemStatus.BACKLOG: frozenset(
        {WorkItemStatus.TODO, WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED}
    ),
    WorkItemStatus.TODO: frozenset(
        {WorkItemStatus.BACKLOG, WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED}
    ),
    WorkItemStatus.IN_PROGRESS: frozenset(
        {
            WorkItemStatus.TODO,
            WorkItemStatus.IN_REVIEW,
            WorkItemStatus.DONE,
            WorkItemStatus.CANCELLED,
        }
    ),
    WorkItemStatus.IN_REVIEW: frozenset(
        {
            WorkItemStatus.IN_PROGRESS,
            WorkItemStatus.DONE,
            WorkItemStatus.CANCELLED,
        }
    ),
    WorkItemStatus.DONE: frozenset({WorkItemStatus.IN_REVIEW}),
    WorkItemStatus.CANCELLED: frozenset({WorkItemStatus.BACKLOG, WorkItemStatus.TODO}),
}


class WorkItemStateMachine:
    """Encapsulates work item status transition rules."""

    @staticmethod
    def can_transition(current: WorkItemStatus, target: WorkItemStatus) -> bool:
        if current == target:
            return False
        return target in _ALLOWED_TRANSITIONS.get(current, frozenset())

    @staticmethod
    def ensure_transition(current: WorkItemStatus, target: WorkItemStatus) -> None:
        if current == target:
            raise BusinessRuleViolationError(
                f"Work item is already in status '{current.value}'"
            )
        if target not in _ALLOWED_TRANSITIONS.get(current, frozenset()):
            raise BusinessRuleViolationError(
                f"Cannot transition work item from '{current.value}' to '{target.value}'"
            )
        if current == WorkItemStatus.DONE and target == WorkItemStatus.BACKLOG:
            raise BusinessRuleViolationError(
                "Completed work items cannot move back to backlog"
            )


def apply_status_change(item: WorkItem, target: WorkItemStatus) -> None:
    """Apply a validated status change with correct timestamp side effects."""
    WorkItemStateMachine.ensure_transition(item.status, target)

    if target == WorkItemStatus.IN_PROGRESS and item.started_at is None:
        item.started_at = datetime.now(timezone.utc)
    if target == WorkItemStatus.DONE:
        item.completed_at = datetime.now(timezone.utc)
    if item.status == WorkItemStatus.DONE and target != WorkItemStatus.DONE:
        # Reopening: clear completion timestamp
        item.completed_at = None

    item.status = target
    item.touch()


def normalize_labels(labels: list[str] | None) -> list[str]:
    """Normalize and de-duplicate labels."""
    if not labels:
        return []
    seen: list[str] = []
    for raw in labels:
        if raw is None:
            continue
        normalized = raw.strip().lower()
        if not normalized:
            continue
        if len(normalized) > 64:
            raise ValidationError("Labels must be 64 characters or fewer")
        if normalized not in seen:
            seen.append(normalized)
    return seen


def ensure_due_date_valid(due_date: date | None, target_end: date | None) -> None:
    """Optional validation for due_date against a project's target end date."""
    if due_date is None or target_end is None:
        return
    if due_date > target_end:
        raise ValidationError(
            "Due date cannot be after the project's target end date"
        )


def ensure_hierarchy(item_type: WorkItemType, epic_id, parent_id) -> None:
    """Validate parent/epic relationships based on the work-item type."""
    if item_type == WorkItemType.EPIC and epic_id is not None:
        raise ValidationError("An epic cannot belong to another epic")
    if parent_id is not None and epic_id is not None and parent_id == epic_id:
        raise ValidationError("parent_id and epic_id must not reference the same item")