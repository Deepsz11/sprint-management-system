"""OKR DTOs."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import OKRStatus, OKRType


class ObjectiveCreateDTO(BaseModel):
    """Payload for creating an objective."""

    team_id: UUID | None = None
    owner_id: UUID | None = None
    parent_id: UUID | None = None
    title: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    okr_type: OKRType = OKRType.TEAM
    period_start: date
    period_end: date

    @model_validator(mode="after")
    def _validate_period(self) -> "ObjectiveCreateDTO":
        if self.period_end < self.period_start:
            raise ValueError("period_end cannot be before period_start")
        if self.okr_type == OKRType.TEAM and self.team_id is None:
            raise ValueError("team_id is required for team-level objectives")
        return self


class ObjectiveUpdateDTO(BaseModel):
    """Payload for updating an objective."""

    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    owner_id: UUID | None = None
    status: OKRStatus | None = None
    period_start: date | None = None
    period_end: date | None = None


class ObjectiveDTO(BaseModel):
    """Objective response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    team_id: UUID | None
    owner_id: UUID | None
    parent_id: UUID | None
    title: str
    description: str | None
    okr_type: OKRType
    status: OKRStatus
    period_start: date
    period_end: date
    created_at: datetime
    updated_at: datetime


class KeyResultCreateDTO(BaseModel):
    """Payload for creating a key result."""

    objective_id: UUID
    kpi_id: UUID | None = None
    title: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    baseline_value: Decimal
    target_value: Decimal
    current_value: Decimal = Decimal("0")
    weight: Decimal = Field(default=Decimal("1"), gt=0)


class KeyResultUpdateDTO(BaseModel):
    """Payload for updating a key result."""

    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    weight: Decimal | None = Field(default=None, gt=0)
    status: OKRStatus | None = None


class KeyResultDTO(BaseModel):
    """Key result response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    objective_id: UUID
    kpi_id: UUID | None
    title: str
    description: str | None
    baseline_value: Decimal
    target_value: Decimal
    current_value: Decimal
    progress_percent: Decimal
    weight: Decimal
    status: OKRStatus
    created_at: datetime
    updated_at: datetime