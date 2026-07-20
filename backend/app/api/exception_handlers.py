"""Central exception handlers for the FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    ApplicationError,
    AuthenticationError,
    AuthorizationError,
    BusinessRuleViolationError,
    ConflictError,
    ExternalServiceError,
    NotFoundError,
    ValidationError,
)
from app.core.logging import get_logger

_logger = get_logger("api.exceptions")


def _payload(code: str, message: str, details: dict | None = None) -> dict:
    return {"error": code, "message": message, "details": details or {}}


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers on the FastAPI application."""

    @app.exception_handler(NotFoundError)
    async def _not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("not_found", exc.message, exc.details),
        )

    @app.exception_handler(ConflictError)
    async def _conflict(_: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("conflict", exc.message, exc.details),
        )

    @app.exception_handler(ValidationError)
    async def _validation(_: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("validation_error", exc.message, exc.details),
        )

    @app.exception_handler(BusinessRuleViolationError)
    async def _business(_: Request, exc: BusinessRuleViolationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("business_rule_violation", exc.message, exc.details),
        )

    @app.exception_handler(AuthenticationError)
    async def _auth(_: Request, exc: AuthenticationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("unauthenticated", exc.message, exc.details),
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(AuthorizationError)
    async def _authz(_: Request, exc: AuthorizationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("forbidden", exc.message, exc.details),
        )

    @app.exception_handler(ExternalServiceError)
    async def _external(_: Request, exc: ExternalServiceError) -> JSONResponse:
        _logger.error("External service error: %s", exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("external_service_error", exc.message, exc.details),
        )

    @app.exception_handler(ApplicationError)
    async def _application(_: Request, exc: ApplicationError) -> JSONResponse:
        _logger.exception("Unhandled application error")
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("application_error", exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def _request_validation(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_payload(
                "request_validation_error",
                "Request validation failed",
                {"errors": exc.errors()},
            ),
        )

    @app.exception_handler(IntegrityError)
    async def _integrity(_: Request, exc: IntegrityError) -> JSONResponse:
        _logger.warning("Database integrity error: %s", exc)
        return JSONResponse(
            status_code=409,
            content=_payload(
                "conflict",
                "The request could not be completed due to a data conflict.",
            ),
        )

    @app.exception_handler(SQLAlchemyError)
    async def _database(_: Request, exc: SQLAlchemyError) -> JSONResponse:
        _logger.exception("Database error")
        return JSONResponse(
            status_code=500,
            content=_payload("database_error", "A database error occurred."),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("http_error", str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        _logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content=_payload("internal_error", "An unexpected error occurred."),
        )