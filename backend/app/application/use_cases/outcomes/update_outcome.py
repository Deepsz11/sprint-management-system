"""Update business outcome use case."""

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
from app.core.exceptions import NotFoundError
from app.domain.entities.business_outcome_extensions import (
    OutcomeLifecycle,
    apply_status_change,
    validate_target_date,
    validate_value_bounds,
)
from app.domain.enums import OutcomeStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateBusinessOutcomeCommand:
    """Update business outcome command."""

    outcome_id: UUID
    context: RequestContext
    name: str | None = None
    description: str | None = None
    hypothesis: str | None = None
    owner_id: UUID | None = None
    status: OutcomeStatus | None = None
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = None
    financial_impact_estimate: Decimal | None = None
    _name_provided: bool = False
    _description_provided: bool = False
    _hypothesis_provided: bool = False
    _owner_provided: bool = False
    _target_date_provided: bool = False
    _baseline_value_provided: bool = False
    _target_value_provided: bool = False
    _current_value_provided: bool = False
    _confidence_score_provided: bool = False
    _financial_impact_provided: bool = False


class UpdateBusinessOutcomeUseCase(
    UseCase[UpdateBusinessOutcomeCommand, BusinessOutcomeDTO]
):
    """Update a business outcome."""

    def execute(
        self, command: UpdateBusinessOutcomeCommand
    ) -> BusinessOutcomeDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(command.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {command.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, outcome.organization_id
            )
            OutcomeLifecycle.ensure_editable(outcome)

            validator = BusinessOutcomeValidator(uow)

            if command._name_provided and command.name is not None:
                validator.ensure_unique_name(
                    outcome.organization_id, command.name, exclude_id=outcome.id
                )
                outcome.name = command.name.strip()

            if command._description_provided:
                outcome.description = command.description
            if command._hypothesis_provided:
                outcome.hypothesis = command.hypothesis

            if command._owner_provided:
                validator.ensure_owner_in_org(command.owner_id, outcome.organization_id)
                outcome.owner_id = command.owner_id

            if command._target_date_provided:
                validate_target_date(command.target_date)
                outcome.target_date = command.target_date

            new_baseline = (
                command.baseline_value
                if command._baseline_value_provided
                else outcome.baseline_value
            )
            new_target = (
                command.target_value
                if command._target_value_provided
                else outcome.target_value
            )
            new_current = (
                command.current_value
                if command._current_value_provided
                else outcome.current_value
            )
            validate_value_bounds(new_baseline, new_target, new_current)

            if command._baseline_value_provided:
                outcome.baseline_value = command.baseline_value
            if command._target_value_provided:
                outcome.target_value = command.target_value
            if command._current_value_provided:
                outcome.current_value = command.current_value
            if command._confidence_score_provided:
                outcome.confidence_score = command.confidence_score
            if command._financial_impact_provided:
                outcome.financial_impact_estimate = command.financial_impact_estimate

            outcome.touch()

            if command.status is not None and command.status != outcome.status:
                apply_status_change(outcome, command.status)

            updated = uow.outcomes.update(outcome)
            uow.commit()
            return outcome_to_dto(updated)