"""Domain service for computing sprint performance metrics."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence

from app.domain.entities.sprint import Sprint
from app.domain.entities.work_item import WorkItem
from app.domain.enums import SprintStatus, WorkItemStatus, WorkItemType


@dataclass(frozen=True)
class SprintMetrics:
    """Aggregated metrics for a sprint."""

    sprint_id: str
    total_items: int
    completed_items: int
    cancelled_items: int
    total_points_planned: int
    total_points_completed: int
    completion_rate: Decimal
    velocity: int
    bug_count: int
    story_count: int
    task_count: int
    scope_change_percent: Decimal


class SprintMetricsDomainService:
    """Compute sprint-level engineering metrics."""

    @staticmethod
    def compute(sprint: Sprint, work_items: Sequence[WorkItem]) -> SprintMetrics:
        """Compute metrics for a sprint given its work items."""
        total_items = len(work_items)
        completed_items = sum(1 for w in work_items if w.status == WorkItemStatus.DONE)
        cancelled_items = sum(
            1 for w in work_items if w.status == WorkItemStatus.CANCELLED
        )
        total_points_planned = sum(w.story_points or 0 for w in work_items)
        total_points_completed = sum(
            (w.story_points or 0) for w in work_items if w.status == WorkItemStatus.DONE
        )
        bug_count = sum(1 for w in work_items if w.item_type == WorkItemType.BUG)
        story_count = sum(1 for w in work_items if w.item_type == WorkItemType.STORY)
        task_count = sum(1 for w in work_items if w.item_type == WorkItemType.TASK)

        completion_rate = (
            (Decimal(total_points_completed) / Decimal(total_points_planned)).quantize(
                Decimal("0.0001")
            )
            if total_points_planned > 0
            else Decimal("0")
        )

        scope_change_percent = (
            (
                Decimal(total_points_planned - sprint.planned_capacity)
                / Decimal(sprint.planned_capacity)
                * Decimal("100")
            ).quantize(Decimal("0.01"))
            if sprint.planned_capacity > 0
            else Decimal("0")
        )

        velocity = total_points_completed if sprint.status == SprintStatus.COMPLETED else 0

        return SprintMetrics(
            sprint_id=str(sprint.id),
            total_items=total_items,
            completed_items=completed_items,
            cancelled_items=cancelled_items,
            total_points_planned=total_points_planned,
            total_points_completed=total_points_completed,
            completion_rate=completion_rate,
            velocity=velocity,
            bug_count=bug_count,
            story_count=story_count,
            task_count=task_count,
            scope_change_percent=scope_change_percent,
        )

    @staticmethod
    def rolling_velocity(sprints: Sequence[Sprint], window: int = 3) -> Decimal:
        """Return average velocity across the last N completed sprints."""
        completed = [s for s in sprints if s.status == SprintStatus.COMPLETED]
        if not completed:
            return Decimal("0")
        completed.sort(key=lambda s: s.completed_at or s.end_date, reverse=True)
        subset = completed[:window]
        total = sum(s.completed_points for s in subset)
        return (Decimal(total) / Decimal(len(subset))).quantize(Decimal("0.01"))