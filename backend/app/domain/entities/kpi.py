"""KPI entity and metric snapshots."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import KPIDirection, KPIUnit


@dataclass
class KPI(SoftDeletableEntity):
    """A Key Performance Indicator tracked by the organization."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str = ""
    description: str | None = None
    unit: KPIUnit = KPIUnit.COUNT
    currency: str | None = None
    direction: KPIDirection = KPIDirection.INCREASE
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = None
    refresh_frequency_hours: int | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("KPI name is required")
        if self.unit == KPIUnit.CURRENCY and not self.currency:
            raise ValidationError("Currency is required for currency-typed KPIs")
        if self.currency:
            code = self.currency.strip().upper()
            if len(code) != 3 or not code.isalpha():
                raise ValidationError(f"Invalid currency code: {self.currency}")
            self.currency = code
        if self.refresh_frequency_hours is not None and self.refresh_frequency_hours <= 0:
            raise ValidationError("Refresh frequency must be positive")

    def record_current_value(self, value: Decimal) -> None:
        self.current_value = value
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()

    def activate(self) -> None:
        self.is_active = True
        self.touch()

    @property
    def delta_from_baseline(self) -> Decimal | None:
        if self.baseline_value is None or self.current_value is None:
            return None
        return self.current_value - self.baseline_value

    @property
    def is_on_track(self) -> bool:
        """Return True when KPI trend matches desired direction."""
        if self.baseline_value is None or self.current_value is None:
            return False
        if self.direction == KPIDirection.INCREASE:
            return self.current_value >= self.baseline_value
        if self.direction == KPIDirection.DECREASE:
            return self.current_value <= self.baseline_value
        # MAINTAIN: within +/- 5% band of baseline
        if self.baseline_value == 0:
            return self.current_value == 0
        tolerance = abs(self.baseline_value) * Decimal("0.05")
        return abs(self.current_value - self.baseline_value) <= tolerance


@dataclass
class MetricSnapshot(SoftDeletableEntity):
    """A point-in-time snapshot of a KPI's value."""

    kpi_id: UUID = field(default_factory=lambda: UUID(int=0))
    value: Decimal = Decimal("0")
    recorded_at: datetime = field(default_factory=datetime.utcnow)
    source: str | None = None
    notes: str | None = None
    context: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            self.value = Decimal(str(self.value))