from __future__ import annotations

"""Project endpoints."""
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.project import ProjectCreateDTO, ProjectDTO, ProjectUpdateDTO
from app.application.mappers import project_to_dto
from app.core.exceptions import ConflictError, NotFoundError
from app.domain.entities.project import Project
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
)
def create_project(
    payload: ProjectCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Create a new project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to create projects",
    )
    if context.organization_id is None:
        raise ConflictError("Project creation requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(payload.team_id)
        if team is None:
            raise NotFoundError(f"Team {payload.team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        if uow.projects.key_exists(context.organization_id, payload.key):
            raise ConflictError(f"Project key '{payload.key}' is already in use")
        if uow.projects.slug_exists(context.organization_id, payload.slug):
            raise ConflictError(f"Project slug '{payload.slug}' is already in use")

        project = Project(
            organization_id=context.organization_id,
            team_id=payload.team_id,
            name=payload.name,
            key=payload.key,
            slug=Slug(payload.slug),
            description=payload.description,
            start_date=payload.start_date,
            target_end_date=payload.target_end_date,
        )
        created = uow.projects.add(project)
        uow.commit()
        return project_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[ProjectDTO],
    status_code=status.HTTP_200_OK,
    summary="List projects",
)
def list_projects(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    team_id: UUID | None = Query(default=None),
    include_archived: bool = Query(default=False),
) -> PaginatedResultDTO[ProjectDTO]:
    """List projects."""
    if context.organization_id is None:
        return PaginatedResultDTO[ProjectDTO](
            items=[], total=0, limit=limit, offset=offset
        )

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        if team_id is not None:
            team = uow.teams.get_by_id(team_id)
            if team is None:
                raise NotFoundError(f"Team {team_id} not found")
            AuthorizationDomainService.ensure_same_organization(
                context.actor, team.organization_id
            )
            items = uow.projects.list_by_team(team_id, page, include_archived)
        else:
            items = uow.projects.list_by_organization(
                context.organization_id, page, include_archived
            )
        total = uow.projects.count_by_organization(
            context.organization_id, include_archived
        )

    return PaginatedResultDTO[ProjectDTO](
        items=[project_to_dto(p) for p in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a project",
)
def get_project(
    project_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Retrieve a project."""
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        return project_to_dto(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a project",
)
def update_project(
    project_id: UUID,
    payload: ProjectUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Update a project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to update projects",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        if payload.name is not None:
            project.rename(payload.name)
        if payload.description is not None:
            project.description = payload.description
            project.touch()
        if payload.start_date is not None:
            project.start_date = payload.start_date
            project.touch()
        if payload.target_end_date is not None:
            project.target_end_date = payload.target_end_date
            project.touch()
        if payload.is_archived is not None:
            if payload.is_archived:
                project.archive()
            else:
                project.unarchive()

        updated = uow.projects.update(project)
        uow.commit()
        return project_to_dto(updated)

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete (soft) a project",
)
def delete_project(
    project_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> Response:
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to delete projects",
    )

    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")

        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        uow.projects.delete(project_id)
        uow.commit()

    return {"message": "Project deleted successfully"}