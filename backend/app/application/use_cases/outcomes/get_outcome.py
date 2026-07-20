"""Get business outcome use case (with linked children)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.business_outcome_extensions import (
    BusinessOutcomeDetailDTO,
)
from app.application.mappers import (
    kpi_to_dto,
    outcome_to_dto,
    work_item_to_dto,
)
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class GetBusinessOutcomeQuery:
    """Query for a single business outcome."""

    outcome_id: UUID
    context: RequestContext
    include_linked: bool = True


class GetBusinessOutcomeUseCase(
    UseCase[GetBusinessOutcomeQuery, BusinessOutcomeDetailDTO]
):
    """Retrieve a business outcome and its linked children."""

    def execute(
        self, query: GetBusinessOutcomeQuery
    ) -> BusinessOutcomeDetailDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.OUTCOME_READ)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(query.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {query.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, outcome.organization_id
            )

            kpis = []
            work_items = []
            attribution_count = 0
            latest_snapshot_at = None

            if query.include_linked:
                kpi_entities = uow.kpis.list_by_outcome(outcome.id)
                kpis = [kpi_to_dto(k) for k in kpi_entities]

                attributions = uow.attributions.list_by_outcome(outcome.id)
                attribution_count = len(attributions)

                seen_ids: set[UUID] = set()
                for attribution in attributions:
                    if attribution.work_item_id is None:
                        continue
                    if attribution.work_item_id in seen_ids:
                        continue
                    seen_ids.add(attribution.work_item_id)
                    item = uow.work_items.get_by_id(attribution.work_item_id)
                    if item is not None:
                        work_items.append(work_item_to_dto(item))

                for kpi in kpi_entities:
                    snapshot = uow.metric_snapshots.latest_for_kpi(kpi.id)
                    if snapshot is None:
                        continue
                    if (
                        latest_snapshot_at is None
                        or snapshot.recorded_at > latest_snapshot_at
                    ):
                        latest_snapshot_at = snapshot.recorded_at

            return BusinessOutcomeDetailDTO(
                outcome=outcome_to_dto(outcome),
                kpis=kpis,
                linked_work_items=work_items,
                attribution_count=attribution_count,
                latest_snapshot_at=latest_snapshot_at,
            )