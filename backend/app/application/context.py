"""Execution context passed to use cases."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.user import User


@dataclass(frozen=True)
class RequestContext:
    """Context capturing the acting user and request metadata."""

    actor: User
    ip_address: str | None = None
    user_agent: str | None = None

    @property
    def actor_id(self) -> UUID:
        return self.actor.id

    @property
    def organization_id(self) -> UUID | None:
        return self.actor.organization_id