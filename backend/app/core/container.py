"""Dependency injection container for application-wide services and factories."""

from __future__ import annotations

from typing import Callable

from app.application.services.audit_service import AuditService
from app.application.services.authentication_service import AuthenticationService
from app.application.services.notification_service import NotificationService
from app.core.config import Settings, get_settings
from app.domain.services.attribution_service import AttributionDomainService
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.outcome_health_service import OutcomeHealthDomainService
from app.domain.services.password_policy import (
    DEFAULT_PASSWORD_POLICY,
    PasswordPolicy,
)
from app.domain.services.permissions import PermissionRegistry
from app.domain.services.sprint_metrics_service import SprintMetricsDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class Container:
    """Application service container.

    Wires up cross-cutting collaborators without introducing external DI
    frameworks. All accessors are safe to call any number of times.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._uow_factory: Callable[[], SQLAlchemyUnitOfWork] = SQLAlchemyUnitOfWork
        self._password_policy: PasswordPolicy = PasswordPolicy(
            min_length=self._settings.PASSWORD_MIN_LENGTH,
            max_length=DEFAULT_PASSWORD_POLICY.max_length,
            require_upper=DEFAULT_PASSWORD_POLICY.require_upper,
            require_lower=DEFAULT_PASSWORD_POLICY.require_lower,
            require_digit=DEFAULT_PASSWORD_POLICY.require_digit,
            require_special=DEFAULT_PASSWORD_POLICY.require_special,
            forbid_whitespace=DEFAULT_PASSWORD_POLICY.forbid_whitespace,
        )
        self._authentication_service = AuthenticationService(self._uow_factory)

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def uow_factory(self) -> Callable[[], SQLAlchemyUnitOfWork]:
        return self._uow_factory

    @property
    def password_policy(self) -> PasswordPolicy:
        return self._password_policy

    @property
    def authentication_service(self) -> AuthenticationService:
        return self._authentication_service

    @property
    def authorization(self) -> type[AuthorizationDomainService]:
        return AuthorizationDomainService

    @property
    def permissions(self) -> type[PermissionRegistry]:
        return PermissionRegistry

    @property
    def attribution(self) -> type[AttributionDomainService]:
        return AttributionDomainService

    @property
    def sprint_metrics(self) -> type[SprintMetricsDomainService]:
        return SprintMetricsDomainService

    @property
    def outcome_health(self) -> type[OutcomeHealthDomainService]:
        return OutcomeHealthDomainService

    def audit_service(self, uow: SQLAlchemyUnitOfWork) -> AuditService:
        """Build an AuditService bound to an open UnitOfWork."""
        return AuditService(uow.audit_logs)

    def notification_service(self, uow: SQLAlchemyUnitOfWork) -> NotificationService:
        """Build a NotificationService bound to an open UnitOfWork."""
        return NotificationService(uow.notifications)


_container: Container | None = None


def get_container() -> Container:
    """Return the process-wide Container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container() -> None:
    """Reset the container (used in tests)."""
    global _container
    _container = None