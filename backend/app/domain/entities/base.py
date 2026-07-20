"""Base entity types shared across the domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class Entity:
    """Base class for all domain entities."""

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        """Update the entity's updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)


@dataclass
class SoftDeletableEntity(Entity):
    """An entity that supports soft deletion."""

    deleted_at: datetime | None = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        if self.deleted_at is None:
            self.deleted_at = datetime.now(timezone.utc)
            self.touch()

    def restore(self) -> None:
        if self.deleted_at is not None:
            self.deleted_at = None
            self.touch()