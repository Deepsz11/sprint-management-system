"""Business outcome DTOs."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import OutcomeStatus


class BusinessOutcomeCreateDTO(BaseModel):
    """Payload for creating a business outcome."""

    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    hypothesis: str | None = Field(default=None, max_length=4000)
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = Field(default=None, ge=0, le=100)
    financial_impact_estimate: Decimal | None = None


class BusinessOutcomeUpdateDTO(BaseModel):
    """Payload for updating a business outcome."""

    owner_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    hypothesis: str | None = Field(default=None, max_length=4000)
    status: OutcomeStatus | None = None
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = Field(default=None, ge=0, le=100)
    financial_impact_estimate: Decimal | None = None


class BusinessOutcomeDTO(BaseModel):
    """Business outcome response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    owner_id: UUID | None
    name: str
    description: str | None
    hypothesis: str | None
    status: OutcomeStatus
    target_date: date | None
    baseline_value: Decimal | None
    target_value: Decimal | None
    current_value: Decimal | None
    progress_percent: Decimal
    confidence_score: Decimal | None
    financial_impact_estimate: Decimal | None
    created_at: datetime
    updated_at: datetime