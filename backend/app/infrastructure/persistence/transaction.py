"""Transaction utilities: decorator + explicit helpers."""

from __future__ import annotations

from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Iterator, TypeVar

from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

T = TypeVar("T")


@contextmanager
def transactional() -> Iterator[SQLAlchemyUnitOfWork]:
    """Open a UnitOfWork and commit on success, rollback on error."""
    uow = SQLAlchemyUnitOfWork()
    with uow:
        try:
            yield uow
            uow.commit()
        except Exception:
            uow.rollback()
            raise


def in_transaction(func: Callable[..., T]) -> Callable[..., T]:
    """Decorate a function to run inside a UnitOfWork transaction.

    The wrapped function must accept a `uow` keyword-only argument.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        with transactional() as uow:
            return func(*args, uow=uow, **kwargs)

    return wrapper