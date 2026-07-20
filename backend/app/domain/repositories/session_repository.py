"""Repository contract for the UserSession aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence
from uuid import UUID

from app.domain.entities.session import UserSession
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class UserSessionRepositoryContract(Repository[UserSession], ABC):
    """Repository contract for user sessions."""

    @abstractmethod
    def get_by_token_hash(self, token_hash: str) -> UserSession | None:
        """Return a session by its refresh-token hash."""

    @abstractmethod
    def list_active_by_user(self, user_id: UUID) -> Sequence[UserSession]:
        """Return all active sessions for a user."""

    @abstractmethod
    def list_by_user(
        self, user_id: UUID, page: PageRequest
    ) -> Sequence[UserSession]:
        """Return all sessions for a user (active or revoked)."""

    @abstractmethod
    def revoke_all_for_user(self, user_id: UUID) -> int:
        """Revoke every active session for a user. Returns count revoked."""

    @abstractmethod
    def purge_expired(self, cutoff: datetime) -> int:
        """Delete sessions expired before the cutoff. Returns count purged."""