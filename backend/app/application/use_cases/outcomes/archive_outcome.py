"""Archive (or restore) a business outcome."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.mappers import outcome_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.enums import OutcomeStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ArchiveBusinessOutcomeCommand:
    """Archive or restore a business outcome."""

    outcome_id: UUID
    context: RequestContext
    archived: bool = True


class ArchiveBusinessOutcomeUseCase(
    UseCase[ArchiveBusinessOutcomeCommand, BusinessOutcomeDTO]
):
    """Archive a business outcome (transition to ABANDONED) or restore it."""

    def execute(
        self, command: ArchiveBusinessOutcomeCommand
    ) -> BusinessOutcomeDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(command.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {command.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, outcome.organization_id
            )

            if command.archived:
                if outcome.status == OutcomeStatus.ABANDONED:
                    raise BusinessRuleViolationError(
                        "Outcome is already archived"
                    )
                if outcome.status == OutcomeStatus.ACHIEVED:
                    raise BusinessRuleViolationError(
                        "Achieved outcomes cannot be archived; keep them for reporting"
                    )
                outcome.abandon()
            else:
                if outcome.status != OutcomeStatus.ABANDONED:
                    raise BusinessRuleViolationError(
                        "Only archived outcomes can be restored"
                    )
                outcome.status = OutcomeStatus.PROPOSED
                outcome.touch()

            updated = uow.outcomes.update(outcome)
            uow.commit()
            return outcome_to_dto(updated)