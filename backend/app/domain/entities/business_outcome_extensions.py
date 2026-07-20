"""Extension helpers for the BusinessOutcome aggregate.

These helpers centralize lifecycle rules (activation, archival, deletion
guards) used by the outcome use cases without modifying the existing
`BusinessOutcome` entity module.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Final

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.enums import OutcomeStatus

_TERMINAL_STATES: Final[frozenset[OutcomeStatus]] = frozenset(
    {OutcomeStatus.ACHIEVED, OutcomeStatus.ABANDONED}
)

_LIVE_STATES: Final[frozenset[OutcomeStatus]] = frozenset(
    {
        OutcomeStatus.PROPOSED,
        OutcomeStatus.ACTIVE,
        OutcomeStatus.AT_RISK,
        OutcomeStatus.OFF_TRACK,
    }
)


class OutcomeLifecycle:
    """Encapsulates lifecycle predicates for a business outcome."""

    @staticmethod
    def is_archived(outcome: BusinessOutcome) -> bool:
        """Return True when the outcome has been archived (abandoned)."""
        return outcome.status == OutcomeStatus.ABANDONED

    @staticmethod
    def is_terminal(outcome: BusinessOutcome) -> bool:
        """Return True when the outcome is in a terminal state."""
        return outcome.status in _TERMINAL_STATES

    @staticmethod
    def is_live(outcome: BusinessOutcome) -> bool:
        """Return True when the outcome is actively tracked."""
        return outcome.status in _LIVE_STATES

    @staticmethod
    def ensure_editable(outcome: BusinessOutcome) -> None:
        """Ensure the outcome may still be edited."""
        if OutcomeLifecycle.is_archived(outcome):
            raise BusinessRuleViolationError(
                "Archived business outcomes are read-only"
            )

    @staticmethod
    def ensure_status_change_allowed(
        outcome: BusinessOutcome, target: OutcomeStatus
    ) -> None:
        """Validate an explicit status change against lifecycle rules."""
        if outcome.status == target:
            raise BusinessRuleViolationError(
                f"Outcome is already in status '{target.value}'"
            )
        if OutcomeLifecycle.is_archived(outcome):
            raise BusinessRuleViolationError(
                "Archived outcomes cannot change status"
            )
        if (
            outcome.status == OutcomeStatus.ACHIEVED
            and target != OutcomeStatus.ACTIVE
        ):
            raise BusinessRuleViolationError(
                "Achieved outcomes can only be reopened as 'active'"
            )


def apply_status_change(outcome: BusinessOutcome, target: OutcomeStatus) -> None:
    """Apply a validated lifecycle transition."""
    OutcomeLifecycle.ensure_status_change_allowed(outcome, target)
    if target == OutcomeStatus.ACTIVE:
        outcome.status = OutcomeStatus.ACTIVE
    elif target == OutcomeStatus.AT_RISK:
        outcome.mark_at_risk()
    elif target == OutcomeStatus.OFF_TRACK:
        outcome.mark_off_track()
    elif target == OutcomeStatus.ACHIEVED:
        outcome.achieve()
    elif target == OutcomeStatus.ABANDONED:
        outcome.abandon()
    else:
        outcome.status = target
    outcome.touch()


def validate_value_bounds(
    baseline: Decimal | None,
    target: Decimal | None,
    current: Decimal | None,
) -> None:
    """Validate the coherence of baseline/target/current values."""
    if baseline is None and target is None and current is None:
        return
    if baseline is not None and target is not None and baseline == target:
        # Zero-span is allowed but must be intentional; enforce that current
        # cannot then contradict the goal.
        if current is not None and current < baseline:
            raise ValidationError(
                "Current value cannot be below baseline when baseline equals target"
            )


def validate_target_date(target_date: date | None, today: date | None = None) -> None:
    """Ensure a target date is not absurdly far in the past."""
    if target_date is None:
        return
    reference = today or date.today()
    # Allow historical values (e.g., importing historic outcomes) but bound the
    # window to a decade to catch obvious data errors.
    if (reference - target_date).days > 3650:
        raise ValidationError("target_date is more than 10 years in the past")