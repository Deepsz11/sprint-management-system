"""Sprint DTOs."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import SprintStatus


class SprintCreateDTO(BaseModel):
    """Payload for creating a sprint."""

    project_id: UUID
    name: str = Field(min_length=1, max_length=200)
    goal: str | None = Field(default=None, max_length=2000)
    start_date: date
    end_date: date
    planned_capacity: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def _validate_dates(self) -> "SprintCreateDTO":
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class SprintUpdateDTO(BaseModel):
    """Payload for updating a sprint."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    goal: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None
    end_date: date | None = None
    planned_capacity: int | None = Field(default=None, ge=0)


class SprintCompleteDTO(BaseModel):
    """Payload for completing a sprint."""

    completed_points: int = Field(ge=0)


class SprintDTO(BaseModel):
    """Sprint response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    goal: str | None
    start_date: date
    end_date: date
    status: SprintStatus
    started_at: datetime | None
    completed_at: datetime | None
    planned_capacity: int
    completed_points: int
    created_at: datetime
    updated_at: datetime