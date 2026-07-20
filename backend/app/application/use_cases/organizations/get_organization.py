"""Get organization use case."""

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
class GetOrganizationQuery:
    """Query for retrieving an organization."""

    organization_id: UUID
    context: RequestContext


class GetOrganizationUseCase(UseCase[GetOrganizationQuery, OrganizationDTO]):
    """Retrieve an organization by ID."""

    def execute(self, query: GetOrganizationQuery) -> OrganizationDTO:
        AuthorizationDomainService.ensure_same_organization(
            query.context.actor, query.organization_id
        )

        with self._uow_factory() as uow:
            organization = uow.organizations.get_by_id(query.organization_id)
            if organization is None:
                raise NotFoundError(f"Organization {query.organization_id} not found")
            return organization_to_dto(organization)