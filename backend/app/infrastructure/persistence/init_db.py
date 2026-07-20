"""Database initialization helpers."""

from __future__ import annotations

from sqlalchemy import text

from app.core.logging import get_logger
from app.infrastructure.persistence.database import get_engine
from app.infrastructure.persistence.models import Base

_logger = get_logger("infrastructure.init_db")


def ensure_extensions() -> None:
    """Ensure required PostgreSQL extensions exist."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))


def create_all() -> None:
    """Create all tables. Prefer Alembic migrations in production."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    _logger.info("Database schema created (create_all).")


def drop_all() -> None:
    """Drop all tables. Use in tests only."""
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    _logger.warning("Database schema dropped (drop_all).")


def check_connection() -> bool:
    """Return True when the database is reachable."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:  # noqa: BLE001 - health check must be defensive
        _logger.error("Database connection failed: %s", exc)
        return False


def dispose_engine() -> None:
    """Dispose the SQLAlchemy engine connection pool."""
    get_engine().dispose()
    _logger.info("Database engine disposed.")