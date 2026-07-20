"""Authentication endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_current_user
from app.application.dtos.auth import RefreshTokenDTO, TokenDTO
from app.application.dtos.user import UserDTO
from app.application.mappers import user_to_dto
from app.application.use_cases.auth import (
    LoginCommand,
    LoginUseCase,
    RefreshTokenCommand,
    RefreshTokenUseCase,
)
from app.domain.entities.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and obtain access + refresh tokens",
)
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenDTO:
    """Authenticate a user with email + password (OAuth2 password flow compatible)."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    use_case = LoginUseCase()
    return use_case.execute(
        LoginCommand(
            email=form_data.username,
            password=form_data.password,
            ip_address=ip,
            user_agent=ua,
        )
    )


@router.post(
    "/refresh",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="Exchange a refresh token for a new access token",
)
def refresh_token(payload: RefreshTokenDTO) -> TokenDTO:
    """Refresh an access token using a valid refresh token."""
    use_case = RefreshTokenUseCase()
    return use_case.execute(RefreshTokenCommand(refresh_token=payload.refresh_token))


@router.get(
    "/me",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    summary="Return the authenticated user",
)
def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserDTO:
    """Return the currently authenticated user."""
    return user_to_dto(current_user)