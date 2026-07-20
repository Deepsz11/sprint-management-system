"""Extended DTOs for KPI operations."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.application.dtos.kpi import KPIDTO, MetricSnapshotDTO
from app.domain.enums import KPIDirection, KPIUnit


class KPIReplaceDTO(BaseModel):
    """Full-replacement (PUT) payload for a KPI."""

    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    unit: KPIUnit
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    direction: KPIDirection
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = Field(default=None, max_length=500)
    refresh_frequency_hours: int | None = Field(default=None, ge=1, le=8760)
    is_active: bool = True


class KPITargetUpdateDTO(BaseModel):
    """Payload for updating a KPI's target value."""

    target_value: Decimal
    reason: str | None = Field(default=None, max_length=1000)


class KPIRecordSnapshotDTO(BaseModel):
    """Payload for recording a KPI snapshot from the API layer."""

    value: Decimal
    recorded_at: datetime | None = None
    source: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)


class KPIHistoryDTO(BaseModel):
    """Aggregated read model for a KPI's snapshot history."""

    model_config = ConfigDict(from_attributes=True)

    kpi: KPIDTO
    snapshots: list[MetricSnapshotDTO]
    count: int
    earliest_at: datetime | None = None
    latest_at: datetime | None = None