"""Business outcome entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import OutcomeStatus


@dataclass
class BusinessOutcome(SoftDeletableEntity):
    """A measurable business outcome that engineering work should influence."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    owner_id: UUID | None = None
    name: str = ""
    description: str | None = None
    hypothesis: str | None = None
    status: OutcomeStatus = OutcomeStatus.PROPOSED
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = None
    financial_impact_estimate: Decimal | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Outcome name is required")
        if len(self.name) > 300:
            raise ValidationError("Outcome name must be 300 characters or fewer")
        if self.confidence_score is not None:
            if self.confidence_score < Decimal("0") or self.confidence_score > Decimal("100"):
                raise ValidationError("Confidence score must be between 0 and 100")

    @property
    def progress_percent(self) -> Decimal:
        """Return progress percentage from baseline toward target."""
        if self.baseline_value is None or self.target_value is None or self.current_value is None:
            return Decimal("0")
        span = self.target_value - self.baseline_value
        if span == 0:
            return Decimal("100") if self.current_value >= self.target_value else Decimal("0")
        achieved = self.current_value - self.baseline_value
        pct = (achieved / span) * Decimal("100")
        if pct < 0:
            return Decimal("0")
        if pct > 100:
            return Decimal("100")
        return pct.quantize(Decimal("0.01"))

    def activate(self) -> None:
        if self.status != OutcomeStatus.PROPOSED:
            raise BusinessRuleViolationError(
                f"Cannot activate outcome from status {self.status.value}"
            )
        self.status = OutcomeStatus.ACTIVE
        self.touch()

    def mark_at_risk(self) -> None:
        self.status = OutcomeStatus.AT_RISK
        self.touch()

    def mark_off_track(self) -> None:
        self.status = OutcomeStatus.OFF_TRACK
        self.touch()

    def achieve(self) -> None:
        self.status = OutcomeStatus.ACHIEVED
        self.touch()

    def abandon(self) -> None:
        self.status = OutcomeStatus.ABANDONED
        self.touch()

    def update_current_value(self, value: Decimal) -> None:
        self.current_value = value
        self.touch()