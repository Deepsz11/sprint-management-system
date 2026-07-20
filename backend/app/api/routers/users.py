"""User endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.user import UserCreateDTO, UserDTO, UserUpdateDTO
from app.application.mappers import user_to_dto
from app.application.use_cases.auth import RegisterCommand, RegisterUseCase
from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.domain.enums import UserRole, UserStatus
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Email
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user (admin operation)",
)
def create_user(
    payload: UserCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Admin-only endpoint to create a new user."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_users(context.actor),
        "You do not have permission to create users",
    )
    org_id = payload.organization_id or context.actor.organization_id
    if org_id is not None:
        AuthorizationDomainService.ensure_same_organization(context.actor, org_id)

    use_case = RegisterUseCase()
    return use_case.execute(
        RegisterCommand(
            email=str(payload.email),
            password=payload.password,
            full_name=payload.full_name,
            organization_id=org_id,
            role=payload.role,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[UserDTO],
    status_code=status.HTTP_200_OK,
    summary="List users in the caller's organization",
)
def list_users(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    role: UserRole | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
) -> PaginatedResultDTO[UserDTO]:
    """List users in the caller's organization."""
    if context.organization_id is None:
        return PaginatedResultDTO[UserDTO](items=[], total=0, limit=limit, offset=offset)

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        if search:
            items = uow.users.search(context.organization_id, search, page)
        elif role is not None:
            items = uow.users.list_by_role(context.organization_id, role.value, page)
        else:
            items = uow.users.list_by_organization(context.organization_id, page)
        total = uow.users.count_by_organization(context.organization_id)

    return PaginatedResultDTO[UserDTO](
        items=[user_to_dto(u) for u in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{user_id}",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a user by ID",
)
def get_user(
    user_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Retrieve a user."""
    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, user.organization_id
        )
        return user_to_dto(user)


@router.patch(
    "/{user_id}",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
)
def update_user(
    user_id: UUID,
    payload: UserUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Update a user's profile, role, or status."""
    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found")

        AuthorizationDomainService.ensure_same_organization(
            context.actor, user.organization_id
        )

        if payload.role is not None or payload.status is not None:
            AuthorizationDomainService.ensure(
                AuthorizationDomainService.can_manage_users(context.actor),
                "You do not have permission to change user role or status",
            )

        if payload.full_name is not None:
            user.full_name = payload.full_name
            user.touch()
        if payload.role is not None:
            user.change_role(payload.role)
        if payload.status is not None:
            if payload.status == UserStatus.ACTIVE:
                user.activate()
            elif payload.status == UserStatus.SUSPENDED:
                user.suspend()
            elif payload.status == UserStatus.DEACTIVATED:
                user.deactivate()

        updated = uow.users.update(user)
        uow.commit()
        return user_to_dto(updated)


@router.post(
    "/invite",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Invite a new user to the caller's organization",
)
def invite_user(
    payload: UserCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Invite a new user by creating an invited account."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_users(context.actor),
        "You do not have permission to invite users",
    )
    if context.organization_id is None:
        raise ConflictError("Inviting requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        if uow.users.email_exists(str(payload.email)):
            raise ConflictError(f"Email {payload.email} is already registered")

        from app.domain.entities.user import User

        user = User(
            email=Email(str(payload.email)),
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
            organization_id=context.organization_id,
            role=payload.role,
            status=UserStatus.INVITED,
            is_email_verified=False,
        )
        created = uow.users.add(user)
        uow.commit()
        return user_to_dto(created)