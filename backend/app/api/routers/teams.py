"""Team endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.organization import TeamCreateDTO, TeamDTO, TeamUpdateDTO
from app.application.mappers import team_to_dto
from app.core.exceptions import ConflictError, NotFoundError
from app.domain.entities.organization import Team
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post(
    "",
    response_model=TeamDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a team in the caller's organization",
)
def create_team(
    payload: TeamCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Create a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to create teams",
    )
    if context.organization_id is None:
        raise ConflictError("Team creation requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        if uow.teams.slug_exists(context.organization_id, payload.slug):
            raise ConflictError(f"Team slug '{payload.slug}' is already in use")

        team = Team(
            organization_id=context.organization_id,
            name=payload.name,
            slug=Slug(payload.slug),
            description=payload.description,
        )
        created = uow.teams.add(team)
        uow.commit()
        return team_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[TeamDTO],
    status_code=status.HTTP_200_OK,
    summary="List teams in the caller's organization",
)
def list_teams(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[TeamDTO]:
    """List teams in the organization."""
    if context.organization_id is None:
        return PaginatedResultDTO[TeamDTO](items=[], total=0, limit=limit, offset=offset)

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        items = uow.teams.list_by_organization(context.organization_id, page)
        total = uow.teams.count_by_organization(context.organization_id)

    return PaginatedResultDTO[TeamDTO](
        items=[team_to_dto(t) for t in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{team_id}",
    response_model=TeamDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a team",
)
def get_team(
    team_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Retrieve a team."""
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        return team_to_dto(team)


@router.patch(
    "/{team_id}",
    response_model=TeamDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a team",
)
def update_team(
    team_id: UUID,
    payload: TeamUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Update a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to update teams",
    )
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )

        if payload.name is not None:
            team.rename(payload.name)
        if payload.description is not None:
            team.description = payload.description
            team.touch()

        updated = uow.teams.update(team)
        uow.commit()
        return team_to_dto(updated)


@router.delete(
    "/{team_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete (soft) a team",
)
def delete_team(
    team_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> None:
    """Soft-delete a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to delete teams",
    )
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        uow.teams.delete(team_id)
        uow.commit()
    return {"message": "Team deleted successfully"}