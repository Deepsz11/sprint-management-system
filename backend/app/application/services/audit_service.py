"""Audit logging application service."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from app.domain.entities.audit_log import AuditLog
from app.domain.enums import AuditAction
from app.domain.repositories.audit_log_repository import AuditLogRepositoryContract


class AuditService:
    """Writes audit log entries via the provided repository."""

    def __init__(self, repository: AuditLogRepositoryContract) -> None:
        self._repository = repository

    def record(
        self,
        *,
        organization_id: UUID,
        actor_id: UUID | None,
        action: AuditAction,
        resource_type: str,
        resource_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        changes: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        """Persist an audit entry."""
        entry = AuditLog(
            organization_id=organization_id,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            changes=changes or {},
            metadata=metadata or {},
        )
        return self._repository.add(entry)