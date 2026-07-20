"""Create business outcome use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.mappers import outcome_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.business_outcome_validator import (
    BusinessOutcomeValidator,
)
from app.core.exceptions import ConflictError
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.entities.business_outcome_extensions import (
    validate_target_date,
    validate_value_bounds,
)
from app.domain.enums import OutcomeStatus
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class CreateBusinessOutcomeCommand:
    """Create business outcome command."""

    name: str
    context: RequestContext
    owner_id: UUID | None = None
    description: str | None = None
    hypothesis: str | None = None
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = None
    financial_impact_estimate: Decimal | None = None


class CreateBusinessOutcomeUseCase(
    UseCase[CreateBusinessOutcomeCommand, BusinessOutcomeDTO]
):
    """Create a business outcome scoped to the caller's organization."""

    def execute(
        self, command: CreateBusinessOutcomeCommand
    ) -> BusinessOutcomeDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        org_id = command.context.organization_id
        if org_id is None:
            raise ConflictError(
                "Outcomes can only be created within an organization context"
            )

        validate_target_date(command.target_date)
        validate_value_bounds(
            command.baseline_value, command.target_value, command.current_value
        )

        with self._uow_factory() as uow:
            validator = BusinessOutcomeValidator(uow)
            validator.ensure_unique_name(org_id, command.name)
            validator.ensure_owner_in_org(command.owner_id, org_id)

            outcome = BusinessOutcome(
                organization_id=org_id,
                owner_id=command.owner_id,
                name=command.name.strip(),
                description=command.description,
                hypothesis=command.hypothesis,
                status=OutcomeStatus.PROPOSED,
                target_date=command.target_date,
                baseline_value=command.baseline_value,
                target_value=command.target_value,
                current_value=command.current_value,
                confidence_score=command.confidence_score,
                financial_impact_estimate=command.financial_impact_estimate,
            )
            created = uow.outcomes.add(outcome)
            uow.commit()
            return outcome_to_dto(created)