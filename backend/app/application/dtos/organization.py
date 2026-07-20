"""Organization and Team DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OrganizationCreateDTO(BaseModel):
    """Payload for creating an organization."""

    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=2, max_length=64)
    description: str | None = Field(default=None, max_length=2000)
    billing_email: EmailStr | None = None


class OrganizationUpdateDTO(BaseModel):
    """Payload for updating an organization."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    billing_email: EmailStr | None = None
    is_active: bool | None = None


class OrganizationDTO(BaseModel):
    """Organization response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: str | None
    billing_email: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TeamCreateDTO(BaseModel):
    """Payload for creating a team."""

    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=2, max_length=64)
    description: str | None = Field(default=None, max_length=2000)


class TeamUpdateDTO(BaseModel):
    """Payload for updating a team."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class TeamDTO(BaseModel):
    """Team response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    slug: str
    description: str | None
    created_at: datetime
    updated_at: datetime