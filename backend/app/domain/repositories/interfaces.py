"""Concrete repository interfaces for each aggregate."""

from __future__ import annotations

from abc import abstractmethod
from datetime import date
from typing import Sequence
from uuid import UUID

from app.domain.entities.attribution import Evidence, OutcomeAttribution
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.entities.kpi import KPI, MetricSnapshot
from app.domain.entities.notification import Notification
from app.domain.entities.okr import KeyResult, Objective
from app.domain.entities.organization import Organization, Team
from app.domain.entities.project import Project
from app.domain.entities.sprint import Sprint
from app.domain.entities.user import TeamMembership, User
from app.domain.entities.work_item import WorkItem
from app.domain.repositories.base import Repository


class OrganizationRepository(Repository[Organization]):
    @abstractmethod
    def get_by_slug(self, slug: str) -> Organization | None: ...

    @abstractmethod
    def list_all(self, limit: int, offset: int) -> Sequence[Organization]: ...


class TeamRepository(Repository[Team]):
    @abstractmethod
    def list_by_organization(self, organization_id: UUID) -> Sequence[Team]: ...

    @abstractmethod
    def get_by_slug(self, organization_id: UUID, slug: str) -> Team | None: ...


class UserRepository(Repository[User]):
    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[User]: ...


class TeamMembershipRepository(Repository[TeamMembership]):
    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[TeamMembership]: ...

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> Sequence[TeamMembership]: ...

    @abstractmethod
    def get_by_team_and_user(
        self, team_id: UUID, user_id: UUID
    ) -> TeamMembership | None: ...


class ProjectRepository(Repository[Project]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[Project]: ...

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[Project]: ...

    @abstractmethod
    def get_by_key(self, organization_id: UUID, key: str) -> Project | None: ...


class SprintRepository(Repository[Sprint]):
    @abstractmethod
    def list_by_project(
        self, project_id: UUID, limit: int, offset: int
    ) -> Sequence[Sprint]: ...

    @abstractmethod
    def get_active_for_project(self, project_id: UUID) -> Sprint | None: ...

    @abstractmethod
    def list_completed_in_range(
        self, organization_id: UUID, start: date, end: date
    ) -> Sequence[Sprint]: ...


class WorkItemRepository(Repository[WorkItem]):
    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[WorkItem]: ...

    @abstractmethod
    def list_by_project(
        self, project_id: UUID, limit: int, offset: int
    ) -> Sequence[WorkItem]: ...

    @abstractmethod
    def list_by_assignee(self, user_id: UUID) -> Sequence[WorkItem]: ...

    @abstractmethod
    def list_unattributed(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[WorkItem]: ...


class BusinessOutcomeRepository(Repository[BusinessOutcome]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[BusinessOutcome]: ...

    @abstractmethod
    def list_off_track(self, organization_id: UUID) -> Sequence[BusinessOutcome]: ...


class KPIRepository(Repository[KPI]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[KPI]: ...

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[KPI]: ...


class MetricSnapshotRepository(Repository[MetricSnapshot]):
    @abstractmethod
    def list_by_kpi(
        self, kpi_id: UUID, limit: int, offset: int
    ) -> Sequence[MetricSnapshot]: ...

    @abstractmethod
    def latest_for_kpi(self, kpi_id: UUID) -> MetricSnapshot | None: ...


class ObjectiveRepository(Repository[Objective]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[Objective]: ...

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[Objective]: ...


class KeyResultRepository(Repository[KeyResult]):
    @abstractmethod
    def list_by_objective(self, objective_id: UUID) -> Sequence[KeyResult]: ...


class AttributionRepository(Repository[OutcomeAttribution]):
    @abstractmethod
    def list_by_work_item(self, work_item_id: UUID) -> Sequence[OutcomeAttribution]: ...

    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[OutcomeAttribution]: ...

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[OutcomeAttribution]: ...

    @abstractmethod
    def list_by_kpi(self, kpi_id: UUID) -> Sequence[OutcomeAttribution]: ...


class EvidenceRepository(Repository[Evidence]):
    @abstractmethod
    def list_by_attribution(self, attribution_id: UUID) -> Sequence[Evidence]: ...


class NotificationRepository(Repository[Notification]):
    @abstractmethod
    def list_by_recipient(
        self, recipient_id: UUID, limit: int, offset: int
    ) -> Sequence[Notification]: ...

    @abstractmethod
    def count_unread(self, recipient_id: UUID) -> int: ...


class AuditLogRepository(Repository[AuditLog]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[AuditLog]: ...

    @abstractmethod
    def list_by_resource(
        self, resource_type: str, resource_id: UUID
    ) -> Sequence[AuditLog]: ...