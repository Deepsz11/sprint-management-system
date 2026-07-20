"""Extension helpers for the KPI aggregate.

These helpers centralize lifecycle predicates and value-change rules used by
the KPI use cases, without modifying the existing `KPI` entity module.
"""

from __future__ import annotations

from decimal import Decimal

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.kpi import KPI


class KPILifecycle:
    """Lifecycle predicates for a KPI."""

    @staticmethod
    def is_active(kpi: KPI) -> bool:
        return kpi.is_active and not kpi.is_deleted

    @staticmethod
    def has_activation_baseline(kpi: KPI) -> bool:
        """Return True when the KPI has been "activated" (baseline is set)."""
        return kpi.baseline_value is not None

    @staticmethod
    def ensure_editable(kpi: KPI) -> None:
        """Ensure the KPI may still be edited (not soft-deleted)."""
        if kpi.is_deleted:
            raise BusinessRuleViolationError("KPI has been deleted")


def ensure_baseline_stable(kpi: KPI, new_baseline: Decimal | None) -> None:
    """Baseline value cannot change after KPI activation."""
    if new_baseline is None:
        return
    if kpi.baseline_value is None:
        return
    if new_baseline != kpi.baseline_value:
        raise BusinessRuleViolationError(
            "Baseline value cannot be changed after KPI activation"
        )


def ensure_target_direction_consistent(
    baseline: Decimal | None, target: Decimal | None, direction: str
) -> None:
    """Validate that target is consistent with the desired direction."""
    if baseline is None or target is None:
        return
    if direction == "increase" and target < baseline:
        raise ValidationError(
            "Target must be greater than or equal to baseline for INCREASE direction"
        )
    if direction == "decrease" and target > baseline:
        raise ValidationError(
            "Target must be less than or equal to baseline for DECREASE direction"
        )


def ensure_currency_matches_unit(unit: str, currency: str | None) -> None:
    """Ensure currency is provided when unit is monetary and omitted otherwise."""
    if unit == "currency" and not currency:
        raise ValidationError("Currency is required for currency-typed KPIs")
    if unit != "currency" and currency:
        raise ValidationError("Currency should only be set for currency-typed KPIs")