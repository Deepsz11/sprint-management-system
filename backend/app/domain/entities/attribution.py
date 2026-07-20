"""Outcome attribution entity - links work items to business outcomes."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import AttributionMethod, AttributionStrength


@dataclass
class OutcomeAttribution(SoftDeletableEntity):
    """Links a work item (or sprint) to a business outcome or KPI."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    work_item_id: UUID | None = None
    sprint_id: UUID | None = None
    outcome_id: UUID | None = None
    kpi_id: UUID | None = None
    key_result_id: UUID | None = None
    attributed_by_id: UUID | None = None
    method: AttributionMethod = AttributionMethod.MANUAL
    strength: AttributionStrength = AttributionStrength.CONTRIBUTING
    weight: Decimal = Decimal("1.0")
    confidence: Decimal = Decimal("50")
    estimated_value: Decimal | None = None
    rationale: str | None = None

    def __post_init__(self) -> None:
        if self.work_item_id is None and self.sprint_id is None:
            raise ValidationError(
                "Attribution must reference at least one of work_item_id or sprint_id"
            )
        if self.outcome_id is None and self.kpi_id is None and self.key_result_id is None:
            raise ValidationError(
                "Attribution must reference an outcome, KPI, or key result"
            )
        for field_name in ("weight", "confidence"):
            val = getattr(self, field_name)
            if not isinstance(val, Decimal):
                setattr(self, field_name, Decimal(str(val)))
        if self.weight <= 0:
            raise ValidationError("Weight must be positive")
        if self.confidence < Decimal("0") or self.confidence > Decimal("100"):
            raise ValidationError("Confidence must be between 0 and 100")

    def update_strength(self, strength: AttributionStrength) -> None:
        self.strength = strength
        self.touch()

    def update_confidence(self, confidence: Decimal) -> None:
        if not isinstance(confidence, Decimal):
            confidence = Decimal(str(confidence))
        if confidence < Decimal("0") or confidence > Decimal("100"):
            raise ValidationError("Confidence must be between 0 and 100")
        self.confidence = confidence
        self.touch()


@dataclass
class Evidence(SoftDeletableEntity):
    """Supporting evidence for an attribution."""

    attribution_id: UUID = field(default_factory=lambda: UUID(int=0))
    author_id: UUID | None = None
    title: str = ""
    content: str = ""
    source_url: str | None = None
    evidence_type: str = "note"

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Evidence title is required")
        if not self.content or not self.content.strip():
            raise ValidationError("Evidence content is required")