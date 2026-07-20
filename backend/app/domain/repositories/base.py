"""Repository protocols - abstract data-access contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from app.domain.entities.base import Entity

TEntity = TypeVar("TEntity", bound=Entity)


class Repository(ABC, Generic[TEntity]):
    """Abstract base repository for entities."""

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> TEntity | None:
        """Retrieve entity by its ID or return None."""

    @abstractmethod
    def add(self, entity: TEntity) -> TEntity:
        """Persist a new entity."""

    @abstractmethod
    def update(self, entity: TEntity) -> TEntity:
        """Persist changes to an existing entity."""

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """Delete (soft or hard) an entity by ID."""

    @abstractmethod
    def exists(self, entity_id: UUID) -> bool:
        """Return True if an entity with the given ID exists."""


class UnitOfWork(ABC):
    """Abstract unit-of-work for transactional consistency."""

    @abstractmethod
    def __enter__(self) -> UnitOfWork: ...

    @abstractmethod
    def __exit__(self, exc_type: object, exc: object, tb: object) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...