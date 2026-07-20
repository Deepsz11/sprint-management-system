"""Work item DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType


class WorkItemCreateDTO(BaseModel):
    """Payload for creating a work item."""

    project_id: UUID
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    external_key: str | None = Field(default=None, max_length=64)
    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    item_type: WorkItemType = WorkItemType.STORY
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    story_points: int | None = Field(default=None, ge=0, le=1000)
    estimated_hours: float | None = Field(default=None, ge=0)
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    labels: list[str] = Field(default_factory=list)


class WorkItemUpdateDTO(BaseModel):
    """Payload for updating a work item."""

    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    priority: WorkItemPriority | None = None
    status: WorkItemStatus | None = None
    story_points: int | None = Field(default=None, ge=0, le=1000)
    estimated_hours: float | None = Field(default=None, ge=0)
    actual_hours: float | None = Field(default=None, ge=0)
    assignee_id: UUID | None = None
    labels: list[str] | None = None


class WorkItemDTO(BaseModel):
    """Work item response DTO."""

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
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime