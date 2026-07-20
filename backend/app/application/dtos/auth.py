"""Authentication DTOs."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class LoginDTO(BaseModel):
    """Login credentials."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenDTO(BaseModel):
    """Access + refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenDTO(BaseModel):
    """Refresh token request."""

    refresh_token: str = Field(min_length=1)