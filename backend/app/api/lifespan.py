"""FastAPI application lifespan handlers (startup / shutdown)."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.core.config import settings
from app.core.container import get_container, reset_container
from app.core.logging import configure_logging, get_logger
from app.infrastructure.persistence.init_db import check_connection, dispose_engine

_logger = get_logger("api.lifespan")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Manage startup and shutdown for the FastAPI application."""
    configure_logging()
    _logger.info(
        "Starting %s v%s (env=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )

    # Warm the DI container so misconfiguration surfaces immediately.
    get_container()

    if not check_connection():
        _logger.error("Database is not reachable at startup.")
    else:
        _logger.info("Database connection verified.")

    try:
        yield
    finally:
        _logger.info("Shutting down %s", settings.APP_NAME)
        dispose_engine()
        reset_container()