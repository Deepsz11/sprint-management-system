"""Session management endpoints: refresh, logout, list active sessions."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.security import get_authenticated_user
from app.application.dtos.auth import RefreshTokenDTO, TokenDTO
from app.application.dtos.auth_extended import (
    ChangePasswordDTO,
    LogoutDTO,
    UserSessionDTO,
)
from app.application.services.authentication_service import AuthenticationService
from app.application.use_cases.auth.change_password import (
    ChangePasswordCommand,
    ChangePasswordUseCase,
)
from app.core.config import settings
from app.domain.entities.user import User
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token/refresh",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="Rotate a refresh token and issue a new access token",
)
def rotate_refresh_token(payload: RefreshTokenDTO, request: Request) -> TokenDTO:
    """Rotate a refresh token by revoking the presented one and issuing a new pair."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    service = AuthenticationService()
    result = service.refresh(payload.refresh_token, ip_address=ip, user_agent=ua)
    return TokenDTO(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        expires_in=result.expires_in,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Log out of the current session",
)
def logout(
    payload: LogoutDTO,
    _user: Annotated[User, Depends(get_authenticated_user)],
) -> None:
    """Revoke the session backing a refresh token."""
    service = AuthenticationService()
    service.logout(payload.refresh_token)


@router.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
    summary="Log out of every active session for the current user",
)
def logout_all(
    user: Annotated[User, Depends(get_authenticated_user)],
) -> None:
    """Revoke every active session for the current user."""
    service = AuthenticationService()
    service.logout_all(user.id)


@router.get(
    "/sessions",
    response_model=list[UserSessionDTO],
    status_code=status.HTTP_200_OK,
    summary="List the current user's sessions",
)
def list_sessions(
    user: Annotated[User, Depends(get_authenticated_user)],
    limit: int = 20,
    offset: int = 0,
) -> list[UserSessionDTO]:
    """Return the current user's sessions."""
    page = PageRequest(
        limit=min(max(limit, 1), settings.MAX_PAGE_SIZE),
        offset=max(offset, 0),
    )
    with SQLAlchemyUnitOfWork() as uow:
        sessions = uow.user_sessions.list_by_user(user.id, page)
    return [
        UserSessionDTO(
            id=s.id,
            user_id=s.user_id,
            issued_at=s.issued_at,
            expires_at=s.expires_at,
            revoked_at=s.revoked_at,
            ip_address=s.ip_address,
            user_agent=s.user_agent,
            last_used_at=s.last_used_at,
            created_at=s.created_at,
        )
        for s in sessions
    ]


@router.post(
    "/password/change",
    status_code=status.HTTP_200_OK,
    summary="Change the current user's password",
)
def change_password(
    payload: ChangePasswordDTO,
    user: Annotated[User, Depends(get_authenticated_user)],
) -> None:
    """Change the current user's password and revoke all sessions."""
    use_case = ChangePasswordUseCase()
    use_case.execute(
        ChangePasswordCommand(
            user_id=user.id,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
    )
    return {"message": "Deleted successfully"}