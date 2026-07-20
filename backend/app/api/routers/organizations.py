"""Organization endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.organization import (
    OrganizationCreateDTO,
    OrganizationDTO,
    OrganizationUpdateDTO,
)
from app.application.use_cases.organizations import (
    CreateOrganizationCommand,
    CreateOrganizationUseCase,
    GetOrganizationQuery,
    GetOrganizationUseCase,
    ListOrganizationsQuery,
    ListOrganizationsUseCase,
    UpdateOrganizationCommand,
    UpdateOrganizationUseCase,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post(
    "",
    response_model=OrganizationDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new organization",
)
def create_organization(
    payload: OrganizationCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> OrganizationDTO:
    """Create a new organization."""
    use_case = CreateOrganizationUseCase()
    return use_case.execute(
        CreateOrganizationCommand(
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            billing_email=str(payload.billing_email) if payload.billing_email else None,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[OrganizationDTO],
    status_code=status.HTTP_200_OK,
    summary="List organizations",
)
def list_organizations(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[OrganizationDTO]:
    """List organizations visible to the caller."""
    use_case = ListOrganizationsUseCase()
    return use_case.execute(
        ListOrganizationsQuery(
            page=PageDTO(limit=limit, offset=offset),
            context=context,
        )
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve an organization by ID",
)
def get_organization(
    organization_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> OrganizationDTO:
    """Retrieve an organization."""
    use_case = GetOrganizationUseCase()
    return use_case.execute(
        GetOrganizationQuery(organization_id=organization_id, context=context)
    )


@router.patch(
    "/{organization_id}",
    response_model=OrganizationDTO,
    status_code=status.HTTP_200_OK,
    summary="Update an organization",
)
def update_organization(
    organization_id: UUID,
    payload: OrganizationUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> OrganizationDTO:
    """Update an organization."""
    use_case = UpdateOrganizationUseCase()
    return use_case.execute(
        UpdateOrganizationCommand(
            organization_id=organization_id,
            name=payload.name,
            description=payload.description,
            billing_email=str(payload.billing_email) if payload.billing_email else None,
            is_active=payload.is_active,
            context=context,
        )
    )