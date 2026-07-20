"""Project entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.value_objects import Slug


@dataclass
class Project(SoftDeletableEntity):
    """A project within a team that groups sprints and work items."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    team_id: UUID = field(default_factory=lambda: UUID(int=0))
    name: str = ""
    key: str = ""
    slug: Slug = field(default_factory=lambda: Slug("default"))
    description: str | None = None
    start_date: date | None = None
    target_end_date: date | None = None
    is_archived: bool = False

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Project name is required")
        if not self.key or len(self.key) < 2 or len(self.key) > 12:
            raise ValidationError("Project key must be between 2 and 12 characters")
        if not self.key.isalnum() or not self.key.isupper():
            raise ValidationError("Project key must be uppercase alphanumeric")
        if self.start_date and self.target_end_date and self.target_end_date < self.start_date:
            raise ValidationError("Target end date cannot be before start date")

    def archive(self) -> None:
        self.is_archived = True
        self.touch()

    def unarchive(self) -> None:
        self.is_archived = False
        self.touch()

    def rename(self, new_name: str) -> None:
        if not new_name.strip():
            raise ValidationError("Project name is required")
        self.name = new_name.strip()
        self.touch()