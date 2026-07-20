"""Domain service for evaluating business outcome health."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.enums import OutcomeStatus


@dataclass(frozen=True)
class OutcomeHealth:
    """Health signal for a business outcome."""

    outcome_id: str
    progress_percent: Decimal
    time_elapsed_percent: Decimal
    health_score: Decimal
    is_at_risk: bool
    is_off_track: bool
    recommended_status: OutcomeStatus


class OutcomeHealthDomainService:
    """Assess whether an outcome is on track, at risk, or off track."""

    AT_RISK_GAP = Decimal("15")
    OFF_TRACK_GAP = Decimal("30")

    @classmethod
    def evaluate(
        cls,
        outcome: BusinessOutcome,
        as_of: date | None = None,
        period_start: date | None = None,
    ) -> OutcomeHealth:
        """Return a health assessment relative to progress vs. time elapsed."""
        today = as_of or date.today()
        progress = outcome.progress_percent

        time_elapsed = Decimal("0")
        if outcome.target_date and period_start:
            total_days = (outcome.target_date - period_start).days
            elapsed_days = (today - period_start).days
            if total_days > 0:
                pct = (Decimal(elapsed_days) / Decimal(total_days)) * Decimal("100")
                time_elapsed = max(Decimal("0"), min(Decimal("100"), pct))
        elif outcome.target_date:
            days_left = (outcome.target_date - today).days
            time_elapsed = (
                Decimal("100") if days_left <= 0 else Decimal("50")
            )

        gap = time_elapsed - progress
        is_off_track = gap >= cls.OFF_TRACK_GAP
        is_at_risk = gap >= cls.AT_RISK_GAP and not is_off_track

        health_score = (Decimal("100") - max(Decimal("0"), gap)).quantize(Decimal("0.01"))

        if outcome.status == OutcomeStatus.ACHIEVED:
            recommended = OutcomeStatus.ACHIEVED
        elif outcome.status == OutcomeStatus.ABANDONED:
            recommended = OutcomeStatus.ABANDONED
        elif is_off_track:
            recommended = OutcomeStatus.OFF_TRACK
        elif is_at_risk:
            recommended = OutcomeStatus.AT_RISK
        elif progress >= Decimal("100"):
            recommended = OutcomeStatus.ACHIEVED
        else:
            recommended = OutcomeStatus.ACTIVE

        return OutcomeHealth(
            outcome_id=str(outcome.id),
            progress_percent=progress,
            time_elapsed_percent=time_elapsed.quantize(Decimal("0.01")),
            health_score=health_score,
            is_at_risk=is_at_risk,
            is_off_track=is_off_track,
            recommended_status=recommended,
        )