"""Sprint endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.sprint import (
    SprintCompleteDTO,
    SprintCreateDTO,
    SprintDTO,
    SprintUpdateDTO,
)
from app.application.mappers import sprint_to_dto
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.entities.sprint import Sprint
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.post(
    "",
    response_model=SprintDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a sprint",
)
def create_sprint(
    payload: SprintCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Create a new sprint."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to create sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(payload.project_id)
        if project is None:
            raise NotFoundError(f"Project {payload.project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        sprint = Sprint(
            project_id=payload.project_id,
            name=payload.name,
            goal=payload.goal,
            start_date=payload.start_date,
            end_date=payload.end_date,
            planned_capacity=payload.planned_capacity,
        )
        created = uow.sprints.add(sprint)
        uow.commit()
        return sprint_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[SprintDTO],
    status_code=status.HTTP_200_OK,
    summary="List sprints for a project",
)
def list_sprints(
    context: Annotated[RequestContext, Depends(get_request_context)],
    project_id: UUID = Query(...),
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[SprintDTO]:
    """List sprints in a project."""
    page = PageRequest(limit=limit, offset=offset, order_by="start_date")
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        items = uow.sprints.list_by_project(project_id, page)
        from app.domain.repositories.specifications import SprintFilter

        total = uow.sprints.count(SprintFilter(project_id=project_id))

    return PaginatedResultDTO[SprintDTO](
        items=[sprint_to_dto(s) for s in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{sprint_id}",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a sprint",
)
def get_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Retrieve a sprint."""
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        return sprint_to_dto(sprint)


@router.patch(
    "/{sprint_id}",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a sprint",
)
def update_sprint(
    sprint_id: UUID,
    payload: SprintUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Update sprint fields."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to update sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        if payload.name is not None:
            sprint.name = payload.name
        if payload.goal is not None:
            sprint.goal = payload.goal
        if payload.start_date is not None:
            sprint.start_date = payload.start_date
        if payload.end_date is not None:
            sprint.end_date = payload.end_date
        if payload.planned_capacity is not None:
            sprint.planned_capacity = payload.planned_capacity
        sprint.touch()

        if sprint.end_date < sprint.start_date:
            raise BusinessRuleViolationError("end_date cannot be before start_date")

        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.post(
    "/{sprint_id}/start",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Start a sprint",
)
def start_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Transition a sprint into the active state."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to start sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        if uow.sprints.get_active_for_project(sprint.project_id) is not None:
            raise BusinessRuleViolationError(
                "Another sprint is already active in this project"
            )
        sprint.start()
        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.post(
    "/{sprint_id}/complete",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Complete a sprint",
)
def complete_sprint(
    sprint_id: UUID,
    payload: SprintCompleteDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Mark a sprint as completed with a final velocity."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to complete sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        sprint.complete(payload.completed_points)
        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.delete(
    "/{sprint_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete (soft) a sprint",
)
def delete_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> None:
    """Soft-delete a sprint."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to delete sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        uow.sprints.delete(sprint_id)
        uow.commit()

    return {"message": "Sprint deleted successfully"}