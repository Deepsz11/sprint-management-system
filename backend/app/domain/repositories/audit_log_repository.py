"""Repository contract for the AuditLog aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import AuditLogFilter, PageRequest


class AuditLogRepositoryContract(Repository[AuditLog], ABC):
    """Repository contract for the AuditLog aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        """Return audit log entries for an organization."""

    @abstractmethod
    def list_by_resource(
        self, resource_type: str, resource_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        """Return audit entries scoped to a specific resource."""

    @abstractmethod
    def list_by_actor(
        self, actor_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        """Return audit entries produced by a user."""

    @abstractmethod
    def find(self, spec: AuditLogFilter, page: PageRequest) -> Sequence[AuditLog]:
        """Return audit log entries matching a filter."""

    @abstractmethod
    def count(self, spec: AuditLogFilter) -> int:
        """Return count of audit entries matching a filter."""