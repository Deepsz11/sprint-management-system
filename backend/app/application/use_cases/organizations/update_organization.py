"""Update organization use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.organization import OrganizationDTO
from app.application.mappers import organization_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService


@dataclass(frozen=True)
class UpdateOrganizationCommand:
    """Update organization command."""

    organization_id: UUID
    name: str | None
    description: str | None
    billing_email: str | None
    is_active: bool | None
    context: RequestContext


class UpdateOrganizationUseCase(UseCase[UpdateOrganizationCommand, OrganizationDTO]):
    """Update an existing organization."""

    def execute(self, command: UpdateOrganizationCommand) -> OrganizationDTO:
        AuthorizationDomainService.ensure(
            AuthorizationDomainService.can_manage_organization(command.context.actor),
            "Only administrators can update organizations",
        )
        AuthorizationDomainService.ensure_same_organization(
            command.context.actor, command.organization_id
        )

        with self._uow_factory() as uow:
            org = uow.organizations.get_by_id(command.organization_id)
            if org is None:
                raise NotFoundError(f"Organization {command.organization_id} not found")

            if command.name is not None:
                org.rename(command.name)
            if command.description is not None:
                org.description = command.description
                org.touch()
            if command.billing_email is not None:
                org.billing_email = command.billing_email
                org.touch()
            if command.is_active is not None:
                if command.is_active:
                    org.activate()
                else:
                    org.deactivate()

            updated = uow.organizations.update(org)
            uow.commit()
            return organization_to_dto(updated)