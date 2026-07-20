"""KPI and metric snapshot DTOs."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import KPIDirection, KPIUnit


class KPICreateDTO(BaseModel):
    """Payload for creating a KPI."""

    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    unit: KPIUnit = KPIUnit.COUNT
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    direction: KPIDirection = KPIDirection.INCREASE
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = Field(default=None, max_length=500)
    refresh_frequency_hours: int | None = Field(default=None, ge=1, le=8760)


class KPIUpdateDTO(BaseModel):
    """Payload for updating a KPI."""

    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    direction: KPIDirection | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = Field(default=None, max_length=500)
    refresh_frequency_hours: int | None = Field(default=None, ge=1, le=8760)
    is_active: bool | None = None


class KPIDTO(BaseModel):
    """KPI response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    outcome_id: UUID | None
    owner_id: UUID | None
    name: str
    description: str | None
    unit: KPIUnit
    currency: str | None
    direction: KPIDirection
    baseline_value: Decimal | None
    target_value: Decimal | None
    current_value: Decimal | None
    data_source: str | None
    refresh_frequency_hours: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MetricSnapshotCreateDTO(BaseModel):
    """Payload for recording a KPI metric snapshot."""

    kpi_id: UUID
    value: Decimal
    recorded_at: datetime | None = None
    source: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)
    context: dict[str, str] = Field(default_factory=dict)


class MetricSnapshotDTO(BaseModel):
    """Metric snapshot response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    kpi_id: UUID
    value: Decimal
    recorded_at: datetime
    source: str | None
    notes: str | None
    context: dict[str, str]
    created_at: datetime