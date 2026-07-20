"""Create organization use case."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.context import RequestContext
from app.application.dtos.organization import OrganizationDTO
from app.application.mappers import organization_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import ConflictError
from app.domain.entities.organization import Organization
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug


@dataclass(frozen=True)
class CreateOrganizationCommand:
    """Create organization command."""

    name: str
    slug: str
    description: str | None
    billing_email: str | None
    context: RequestContext


class CreateOrganizationUseCase(UseCase[CreateOrganizationCommand, OrganizationDTO]):
    """Create a new organization."""

    def execute(self, command: CreateOrganizationCommand) -> OrganizationDTO:
        AuthorizationDomainService.ensure(
            AuthorizationDomainService.can_manage_organization(command.context.actor),
            "Only administrators can create organizations",
        )

        with self._uow_factory() as uow:
            if uow.organizations.slug_exists(command.slug):
                raise ConflictError(f"Organization slug '{command.slug}' is already in use")

            organization = Organization(
                name=command.name,
                slug=Slug(command.slug),
                description=command.description,
                billing_email=command.billing_email,
                is_active=True,
            )
            created = uow.organizations.add(organization)
            uow.commit()
            return organization_to_dto(created)