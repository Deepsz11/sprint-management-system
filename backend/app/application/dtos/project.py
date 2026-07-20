"""Project DTOs."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectCreateDTO(BaseModel):
    """Payload for creating a project."""

    team_id: UUID
    name: str = Field(min_length=1, max_length=200)
    key: str = Field(min_length=2, max_length=12)
    slug: str = Field(min_length=2, max_length=64)
    description: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None
    target_end_date: date | None = None

    @field_validator("key")
    @classmethod
    def _uppercase_key(cls, v: str) -> str:
        return v.upper()


class ProjectUpdateDTO(BaseModel):
    """Payload for updating a project."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None
    target_end_date: date | None = None
    is_archived: bool | None = None


class ProjectDTO(BaseModel):
    """Project response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    team_id: UUID
    name: str
    key: str
    slug: str
    description: str | None
    start_date: date | None
    target_end_date: date | None
    is_archived: bool
    created_at: datetime
    updated_at: datetime