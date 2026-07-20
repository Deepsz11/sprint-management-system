"""Organization aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.value_objects import Slug


@dataclass
class Organization(SoftDeletableEntity):
    """A tenant organization within the multi-tenant system."""

    name: str = ""
    slug: Slug = field(default_factory=lambda: Slug("default"))
    description: str | None = None
    billing_email: str | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Organization name is required")
        if len(self.name) > 200:
            raise ValidationError("Organization name must be 200 characters or fewer")

    def rename(self, new_name: str) -> None:
        if not new_name or not new_name.strip():
            raise ValidationError("Organization name is required")
        self.name = new_name.strip()
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()

    def activate(self) -> None:
        self.is_active = True
        self.touch()


@dataclass
class Team(SoftDeletableEntity):
    """A team within an organization."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    name: str = ""
    slug: Slug = field(default_factory=lambda: Slug("default"))
    description: str | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Team name is required")
        if self.organization_id == UUID(int=0):
            raise ValidationError("Team must belong to an organization")

    def rename(self, new_name: str) -> None:
        if not new_name or not new_name.strip():
            raise ValidationError("Team name is required")
        self.name = new_name.strip()
        self.touch()