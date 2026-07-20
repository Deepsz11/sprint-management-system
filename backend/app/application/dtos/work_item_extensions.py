"""Extended DTOs for Work Item operations (assign, move, status)."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType


class WorkItemAssignDTO(BaseModel):
    """Payload for reassigning a work item."""

    assignee_id: UUID | None = None


class WorkItemStatusChangeDTO(BaseModel):
    """Payload for changing a work item's status."""

    status: WorkItemStatus
    actual_hours: float | None = Field(default=None, ge=0)


class WorkItemMoveDTO(BaseModel):
    """Payload for moving a work item to a sprint (or unassigning)."""

    sprint_id: UUID | None = None


class WorkItemReplaceDTO(BaseModel):
    """Full-replacement (PUT) payload for a work item."""

    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    item_type: WorkItemType
    priority: WorkItemPriority
    status: WorkItemStatus
    story_points: int | None = Field(default=None, ge=0, le=1000)
    estimated_hours: float | None = Field(default=None, ge=0)
    actual_hours: float | None = Field(default=None, ge=0)
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    assignee_id: UUID | None = None
    labels: list[str] = Field(default_factory=list)
    due_date: date | None = None


class WorkItemDetailDTO(BaseModel):
    """Extended read model for a work item."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    sprint_id: UUID | None
    parent_id: UUID | None
    epic_id: UUID | None
    external_key: str | None
    title: str
    description: str | None
    item_type: WorkItemType
    status: WorkItemStatus
    priority: WorkItemPriority
    story_points: int | None
    estimated_hours: float | None
    actual_hours: float | None
    assignee_id: UUID | None
    reporter_id: UUID | None
    labels: list[str]
    due_date: date | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime