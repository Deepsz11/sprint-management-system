"""SQLAlchemy Unit of Work implementation."""

from __future__ import annotations

from types import TracebackType
from typing import Type

from sqlalchemy.orm import Session

from app.domain.repositories.base import UnitOfWork
from app.infrastructure.persistence.database import SessionFactory
from app.infrastructure.persistence.repositories import (
    SQLAlchemyAttributionRepository,
    SQLAlchemyAuditLogRepository,
    SQLAlchemyBusinessOutcomeRepository,
    SQLAlchemyEvidenceRepository,
    SQLAlchemyKPIRepository,
    SQLAlchemyKeyResultRepository,
    SQLAlchemyMetricSnapshotRepository,
    SQLAlchemyNotificationRepository,
    SQLAlchemyObjectiveRepository,
    SQLAlchemyOrganizationRepository,
    SQLAlchemyProjectRepository,
    SQLAlchemySprintRepository,
    SQLAlchemyTeamMembershipRepository,
    SQLAlchemyTeamRepository,
    SQLAlchemyUserRepository,
    SQLAlchemyWorkItemRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    """Transactional unit of work exposing all repositories."""

    def __init__(self) -> None:
        self._session: Session | None = None
        self.organizations: SQLAlchemyOrganizationRepository
        self.teams: SQLAlchemyTeamRepository
        self.users: SQLAlchemyUserRepository
        self.team_memberships: SQLAlchemyTeamMembershipRepository
        self.projects: SQLAlchemyProjectRepository
        self.sprints: SQLAlchemySprintRepository
        self.work_items: SQLAlchemyWorkItemRepository
        self.outcomes: SQLAlchemyBusinessOutcomeRepository
        self.kpis: SQLAlchemyKPIRepository
        self.metric_snapshots: SQLAlchemyMetricSnapshotRepository
        self.objectives: SQLAlchemyObjectiveRepository
        self.key_results: SQLAlchemyKeyResultRepository
        self.attributions: SQLAlchemyAttributionRepository
        self.evidence: SQLAlchemyEvidenceRepository
        self.notifications: SQLAlchemyNotificationRepository
        self.audit_logs: SQLAlchemyAuditLogRepository

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("UnitOfWork is not active; use it as a context manager")
        return self._session

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        self._session = SessionFactory()
        self._build_repositories(self._session)
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc is not None:
                self.rollback()
        finally:
            if self._session is not None:
                self._session.close()
            self._session = None

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def _build_repositories(self, session: Session) -> None:
        self.organizations = SQLAlchemyOrganizationRepository(session)
        self.teams = SQLAlchemyTeamRepository(session)
        self.users = SQLAlchemyUserRepository(session)
        self.team_memberships = SQLAlchemyTeamMembershipRepository(session)
        self.projects = SQLAlchemyProjectRepository(session)
        self.sprints = SQLAlchemySprintRepository(session)
        self.work_items = SQLAlchemyWorkItemRepository(session)
        self.outcomes = SQLAlchemyBusinessOutcomeRepository(session)
        self.kpis = SQLAlchemyKPIRepository(session)
        self.metric_snapshots = SQLAlchemyMetricSnapshotRepository(session)
        self.objectives = SQLAlchemyObjectiveRepository(session)
        self.key_results = SQLAlchemyKeyResultRepository(session)
        self.attributions = SQLAlchemyAttributionRepository(session)
        self.evidence = SQLAlchemyEvidenceRepository(session)
        self.notifications = SQLAlchemyNotificationRepository(session)
        self.audit_logs = SQLAlchemyAuditLogRepository(session)