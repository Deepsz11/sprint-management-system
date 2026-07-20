"""Audit log entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import Entity
from app.domain.enums import AuditAction


@dataclass
class AuditLog(Entity):
    """An immutable audit event."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    actor_id: UUID | None = None
    action: AuditAction = AuditAction.CREATE
    resource_type: str = ""
    resource_id: UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    changes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.resource_type or not self.resource_type.strip():
            raise ValidationError("resource_type is required")