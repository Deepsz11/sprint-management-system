"""Domain value objects - immutable primitives with validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal

from app.core.exceptions import ValidationError

_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
_SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class Email:
    """A validated email address."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not _EMAIL_REGEX.match(normalized):
            raise ValidationError(f"Invalid email address: {self.value}")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Slug:
    """A URL-safe slug identifier."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not _SLUG_REGEX.match(normalized):
            raise ValidationError(
                f"Invalid slug: {self.value}. Must be lowercase alphanumeric with hyphens."
            )
        if len(normalized) > 64:
            raise ValidationError("Slug must be 64 characters or fewer")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DateRange:
    """An inclusive date range with a start and end."""

    start: date
    end: date

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValidationError("End date cannot be before start date")

    def contains(self, target: date) -> bool:
        return self.start <= target <= self.end

    def overlaps(self, other: DateRange) -> bool:
        return not (self.end < other.start or other.end < self.start)

    @property
    def duration_days(self) -> int:
        return (self.end - self.start).days + 1


@dataclass(frozen=True, slots=True)
class MonetaryAmount:
    """A monetary amount with currency."""

    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        currency = self.currency.strip().upper()
        if len(currency) != 3 or not currency.isalpha():
            raise ValidationError(f"Invalid currency code: {self.currency}")
        object.__setattr__(self, "currency", currency)

    def __add__(self, other: MonetaryAmount) -> MonetaryAmount:
        if self.currency != other.currency:
            raise ValidationError("Cannot add amounts with different currencies")
        return MonetaryAmount(self.amount + other.amount, self.currency)


@dataclass(frozen=True, slots=True)
class MetricValue:
    """A recorded metric value at a point in time."""

    value: Decimal
    recorded_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, "value", Decimal(str(self.value)))
        if self.recorded_at.tzinfo is None:
            object.__setattr__(
                self, "recorded_at", self.recorded_at.replace(tzinfo=timezone.utc)
            )


@dataclass(frozen=True, slots=True)
class Percentage:
    """A percentage value between 0 and 100."""

    value: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, "value", Decimal(str(self.value)))
        if self.value < Decimal("0") or self.value > Decimal("100"):
            raise ValidationError(f"Percentage must be between 0 and 100, got {self.value}")

    def as_ratio(self) -> Decimal:
        return self.value / Decimal("100")