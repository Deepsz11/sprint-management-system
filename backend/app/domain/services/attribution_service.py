"""Domain service for computing outcome attribution and impact."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence

from app.domain.entities.attribution import OutcomeAttribution
from app.domain.entities.sprint import Sprint
from app.domain.entities.work_item import WorkItem
from app.domain.enums import AttributionStrength, SprintStatus, WorkItemStatus


_STRENGTH_WEIGHTS: dict[AttributionStrength, Decimal] = {
    AttributionStrength.PRIMARY: Decimal("1.0"),
    AttributionStrength.CONTRIBUTING: Decimal("0.6"),
    AttributionStrength.SUPPORTING: Decimal("0.3"),
    AttributionStrength.NONE: Decimal("0.0"),
}


@dataclass(frozen=True)
class ImpactScore:
    """Computed impact for a set of attributions."""

    total_score: Decimal
    weighted_confidence: Decimal
    estimated_value: Decimal
    attribution_count: int


class AttributionDomainService:
    """Pure domain logic for reasoning about attribution."""

    @staticmethod
    def strength_factor(strength: AttributionStrength) -> Decimal:
        return _STRENGTH_WEIGHTS[strength]

    @classmethod
    def compute_impact(cls, attributions: Sequence[OutcomeAttribution]) -> ImpactScore:
        """Compute an aggregate impact score across attributions."""
        if not attributions:
            return ImpactScore(
                total_score=Decimal("0"),
                weighted_confidence=Decimal("0"),
                estimated_value=Decimal("0"),
                attribution_count=0,
            )

        total_score = Decimal("0")
        total_weight = Decimal("0")
        weighted_confidence = Decimal("0")
        estimated_value = Decimal("0")

        for attr in attributions:
            factor = cls.strength_factor(attr.strength)
            score = attr.weight * factor * (attr.confidence / Decimal("100"))
            total_score += score
            total_weight += attr.weight
            weighted_confidence += attr.confidence * attr.weight
            if attr.estimated_value is not None:
                estimated_value += attr.estimated_value

        avg_confidence = (
            weighted_confidence / total_weight if total_weight > 0 else Decimal("0")
        )

        return ImpactScore(
            total_score=total_score.quantize(Decimal("0.0001")),
            weighted_confidence=avg_confidence.quantize(Decimal("0.01")),
            estimated_value=estimated_value.quantize(Decimal("0.01")),
            attribution_count=len(attributions),
        )

    @staticmethod
    def find_unattributed_completed_items(
        work_items: Sequence[WorkItem],
        attributions_by_work_item: dict,
    ) -> list[WorkItem]:
        """Return completed work items that have no attributions."""
        return [
            item
            for item in work_items
            if item.status == WorkItemStatus.DONE
            and not attributions_by_work_item.get(item.id)
        ]

    @staticmethod
    def sprint_roi(
        sprint: Sprint,
        attributions: Sequence[OutcomeAttribution],
        estimated_cost: Decimal,
    ) -> Decimal:
        """Compute ROI as (estimated_value - cost) / cost for a completed sprint."""
        if sprint.status != SprintStatus.COMPLETED:
            return Decimal("0")
        if estimated_cost <= 0:
            return Decimal("0")
        total_value = sum(
            (a.estimated_value for a in attributions if a.estimated_value is not None),
            start=Decimal("0"),
        )
        roi = (total_value - estimated_cost) / estimated_cost
        return roi.quantize(Decimal("0.0001"))