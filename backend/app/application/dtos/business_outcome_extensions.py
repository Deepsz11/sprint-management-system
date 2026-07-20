"""Extended DTOs for business outcome operations."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.application.dtos.kpi import KPIDTO
from app.application.dtos.work_item import WorkItemDTO
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.domain.enums import OutcomeStatus


class BusinessOutcomeReplaceDTO(BaseModel):
    """Full-replacement (PUT) payload for a business outcome."""

    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    hypothesis: str | None = Field(default=None, max_length=4000)
    status: OutcomeStatus
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = Field(default=None, ge=0, le=100)
    financial_impact_estimate: Decimal | None = None


class BusinessOutcomeArchiveDTO(BaseModel):
    """Payload for archiving/unarchiving a business outcome."""

    archived: bool = True


class BusinessOutcomeDetailDTO(BaseModel):
    """Aggregated read model for a business outcome with linked children."""

    model_config = ConfigDict(from_attributes=True)

    outcome: BusinessOutcomeDTO
    kpis: list[KPIDTO]
    linked_work_items: list[WorkItemDTO]
    attribution_count: int
    latest_snapshot_at: datetime | None = None