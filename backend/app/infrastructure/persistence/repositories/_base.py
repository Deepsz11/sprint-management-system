"""Shared helpers for SQLAlchemy repositories."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Select, desc
from sqlalchemy.sql.elements import ColumnElement

from app.domain.repositories.specifications import PageRequest


def apply_pagination(
    stmt: Select[Any], page: PageRequest, order_column: ColumnElement[Any]
) -> Select[Any]:
    """Apply ordering, limit, and offset to a select statement."""
    order = desc(order_column) if page.descending else order_column
    return stmt.order_by(order).limit(page.limit).offset(page.offset)


def utcnow() -> datetime:
    """Return the current UTC datetime with timezone information."""
    return datetime.now(timezone.utc)