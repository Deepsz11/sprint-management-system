"""Delete business outcome use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.use_cases.base import UseCase
from app.application.validators.business_outcome_validator import (
    BusinessOutcomeValidator,
)
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class DeleteBusinessOutcomeCommand:
    """Soft-delete a business outcome."""

    outcome_id: UUID
    context: RequestContext


class DeleteBusinessOutcomeUseCase(UseCase[DeleteBusinessOutcomeCommand, None]):
    """Delete a business outcome after enforcing business rules."""

    def execute(self, command: DeleteBusinessOutcomeCommand) -> None:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(command.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {command.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, outcome.organization_id
            )

            attributions = uow.attributions.list_by_outcome(outcome.id)
            if attributions:
                raise BusinessRuleViolationError(
                    "Cannot delete an outcome that has attributions; archive it instead"
                )

            BusinessOutcomeValidator(uow).ensure_deletable(outcome.id)

            # Detach any linked KPIs so they remain usable at the organization level.
            for kpi in uow.kpis.list_by_outcome(outcome.id):
                kpi.outcome_id = None
                kpi.touch()
                uow.kpis.update(kpi)

            uow.outcomes.delete(outcome.id)
            uow.commit()