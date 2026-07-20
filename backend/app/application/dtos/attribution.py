"""Attribution and evidence DTOs."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import AttributionMethod, AttributionStrength


class AttributionCreateDTO(BaseModel):
    """Payload for creating an outcome attribution."""

    work_item_id: UUID | None = None
    sprint_id: UUID | None = None
    outcome_id: UUID | None = None
    kpi_id: UUID | None = None
    key_result_id: UUID | None = None
    method: AttributionMethod = AttributionMethod.MANUAL
    strength: AttributionStrength = AttributionStrength.CONTRIBUTING
    weight: Decimal = Field(default=Decimal("1"), gt=0)
    confidence: Decimal = Field(default=Decimal("50"), ge=0, le=100)
    estimated_value: Decimal | None = None
    rationale: str | None = Field(default=None, max_length=4000)

    @model_validator(mode="after")
    def _validate_relations(self) -> "AttributionCreateDTO":
        if self.work_item_id is None and self.sprint_id is None:
            raise ValueError("At least one of work_item_id or sprint_id is required")
        if self.outcome_id is None and self.kpi_id is None and self.key_result_id is None:
            raise ValueError(
                "At least one of outcome_id, kpi_id, or key_result_id is required"
            )
        return self


class AttributionUpdateDTO(BaseModel):
    """Payload for updating an attribution."""

    strength: AttributionStrength | None = None
    weight: Decimal | None = Field(default=None, gt=0)
    confidence: Decimal | None = Field(default=None, ge=0, le=100)
    estimated_value: Decimal | None = None
    rationale: str | None = Field(default=None, max_length=4000)


class AttributionDTO(BaseModel):
    """Attribution response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    work_item_id: UUID | None
    sprint_id: UUID | None
    outcome_id: UUID | None
    kpi_id: UUID | None
    key_result_id: UUID | None
    attributed_by_id: UUID | None
    method: AttributionMethod
    strength: AttributionStrength
    weight: Decimal
    confidence: Decimal
    estimated_value: Decimal | None
    rationale: str | None
    created_at: datetime
    updated_at: datetime


class EvidenceCreateDTO(BaseModel):
    """Payload for creating evidence."""

    attribution_id: UUID
    title: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1, max_length=10000)
    source_url: str | None = Field(default=None, max_length=2000)
    evidence_type: str = Field(default="note", max_length=32)


class EvidenceDTO(BaseModel):
    """Evidence response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    attribution_id: UUID
    author_id: UUID | None
    title: str
    content: str
    source_url: str | None
    evidence_type: str
    created_at: datetime
    updated_at: datetime