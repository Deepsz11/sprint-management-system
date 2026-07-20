"""Base classes for application use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class UseCase(ABC, Generic[TCommand, TResult]):
    """Base use case protocol."""

    def __init__(self, uow_factory: type[SQLAlchemyUnitOfWork] = SQLAlchemyUnitOfWork) -> None:
        self._uow_factory = uow_factory

    @abstractmethod
    def execute(self, command: TCommand) -> TResult:
        """Execute the use case."""