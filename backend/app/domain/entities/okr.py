"""OKR (Objectives and Key Results) entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import OKRStatus, OKRType


@dataclass
class Objective(SoftDeletableEntity):
    """A qualitative goal to be achieved in a period."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    team_id: UUID | None = None
    owner_id: UUID | None = None
    parent_id: UUID | None = None
    title: str = ""
    description: str | None = None
    okr_type: OKRType = OKRType.TEAM
    status: OKRStatus = OKRStatus.DRAFT
    period_start: date = field(default_factory=date.today)
    period_end: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Objective title is required")
        if self.period_end < self.period_start:
            raise ValidationError("Period end cannot be before period start")
        if self.okr_type == OKRType.TEAM and self.team_id is None:
            raise ValidationError("Team objectives require a team_id")

    def activate(self) -> None:
        if self.status != OKRStatus.DRAFT:
            raise BusinessRuleViolationError(
                f"Cannot activate objective from status {self.status.value}"
            )
        self.status = OKRStatus.ACTIVE
        self.touch()

    def achieve(self) -> None:
        self.status = OKRStatus.ACHIEVED
        self.touch()

    def miss(self) -> None:
        self.status = OKRStatus.MISSED
        self.touch()

    def cancel(self) -> None:
        self.status = OKRStatus.CANCELLED
        self.touch()


@dataclass
class KeyResult(SoftDeletableEntity):
    """A measurable outcome that indicates progress on an objective."""

    objective_id: UUID = field(default_factory=lambda: UUID(int=0))
    kpi_id: UUID | None = None
    title: str = ""
    description: str | None = None
    baseline_value: Decimal = Decimal("0")
    target_value: Decimal = Decimal("0")
    current_value: Decimal = Decimal("0")
    weight: Decimal = Decimal("1")
    status: OKRStatus = OKRStatus.ACTIVE

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Key result title is required")
        for field_name in ("baseline_value", "target_value", "current_value", "weight"):
            val = getattr(self, field_name)
            if not isinstance(val, Decimal):
                setattr(self, field_name, Decimal(str(val)))
        if self.weight <= 0:
            raise ValidationError("Weight must be positive")

    @property
    def progress_percent(self) -> Decimal:
        span = self.target_value - self.baseline_value
        if span == 0:
            return (
                Decimal("100")
                if self.current_value >= self.target_value
                else Decimal("0")
            )
        achieved = self.current_value - self.baseline_value
        pct = (achieved / span) * Decimal("100")
        if pct < 0:
            return Decimal("0")
        if pct > 100:
            return Decimal("100")
        return pct.quantize(Decimal("0.01"))

    def update_current_value(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        self.current_value = value
        self.touch()