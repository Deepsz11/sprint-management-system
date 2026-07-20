"""Domain ↔ ORM mappers."""

from __future__ import annotations

from decimal import Decimal
from typing import cast

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
from app.domain.enums import (
    AttributionMethod,
    AttributionStrength,
    AuditAction,
    KPIDirection,
    KPIUnit,
    NotificationChannel,
    NotificationStatus,
    OKRStatus,
    OKRType,
    OutcomeStatus,
    SprintStatus,
    UserRole,
    UserStatus,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemType,
)
from app.domain.value_objects import Email, Slug
from app.infrastructure.persistence.models.attribution import (
    EvidenceModel,
    OutcomeAttributionModel,
)
from app.infrastructure.persistence.models.audit_log import AuditLogModel
from app.infrastructure.persistence.models.business_outcome import BusinessOutcomeModel
from app.infrastructure.persistence.models.kpi import KPIModel, MetricSnapshotModel
from app.infrastructure.persistence.models.notification import NotificationModel
from app.infrastructure.persistence.models.okr import KeyResultModel, ObjectiveModel
from app.infrastructure.persistence.models.organization import (
    OrganizationModel,
    TeamModel,
)
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.models.sprint import SprintModel
from app.infrastructure.persistence.models.user import (
    TeamMembershipModel,
    UserModel,
)
from app.infrastructure.persistence.models.work_item import WorkItemModel


class OrganizationMapper:
    @staticmethod
    def to_entity(m: OrganizationModel) -> Organization:
        return Organization(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            name=m.name,
            slug=Slug(m.slug),
            description=m.description,
            billing_email=m.billing_email,
            is_active=m.is_active,
        )

    @staticmethod
    def to_model(e: Organization, m: OrganizationModel | None = None) -> OrganizationModel:
        m = m or OrganizationModel()
        m.id = e.id
        m.name = e.name
        m.slug = str(e.slug)
        m.description = e.description
        m.billing_email = e.billing_email
        m.is_active = e.is_active
        m.deleted_at = e.deleted_at
        return m


class TeamMapper:
    @staticmethod
    def to_entity(m: TeamModel) -> Team:
        return Team(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            organization_id=m.organization_id,
            name=m.name,
            slug=Slug(m.slug),
            description=m.description,
        )

    @staticmethod
    def to_model(e: Team, m: TeamModel | None = None) -> TeamModel:
        m = m or TeamModel()
        m.id = e.id
        m.organization_id = e.organization_id
        m.name = e.name
        m.slug = str(e.slug)
        m.description = e.description
        m.deleted_at = e.deleted_at
        return m


class UserMapper:
    @staticmethod
    def to_entity(m: UserModel) -> User:
        return User(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            email=Email(m.email),
            hashed_password=m.hashed_password,
            full_name=m.full_name,
            organization_id=m.organization_id,
            role=UserRole(m.role),
            status=UserStatus(m.status),
            last_login_at=m.last_login_at,
            is_email_verified=m.is_email_verified,
        )

    @staticmethod
    def to_model(e: User, m: UserModel | None = None) -> UserModel:
        m = m or UserModel()
        m.id = e.id
        m.email = str(e.email)
        m.hashed_password = e.hashed_password
        m.full_name = e.full_name
        m.organization_id = e.organization_id
        m.role = e.role.value
        m.status = e.status.value
        m.last_login_at = e.last_login_at
        m.is_email_verified = e.is_email_verified
        m.deleted_at = e.deleted_at
        return m


class TeamMembershipMapper:
    @staticmethod
    def to_entity(m: TeamMembershipModel) -> TeamMembership:
        return TeamMembership(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            team_id=m.team_id,
            user_id=m.user_id,
            is_lead=m.is_lead,
        )

    @staticmethod
    def to_model(
        e: TeamMembership, m: TeamMembershipModel | None = None
    ) -> TeamMembershipModel:
        m = m or TeamMembershipModel()
        m.id = e.id
        m.team_id = e.team_id
        m.user_id = e.user_id
        m.is_lead = e.is_lead
        m.deleted_at = e.deleted_at
        return m


class ProjectMapper:
    @staticmethod
    def to_entity(m: ProjectModel) -> Project:
        return Project(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            organization_id=m.organization_id,
            team_id=m.team_id,
            name=m.name,
            key=m.key,
            slug=Slug(m.slug),
            description=m.description,
            start_date=m.start_date,
            target_end_date=m.target_end_date,
            is_archived=m.is_archived,
        )

    @staticmethod
    def to_model(e: Project, m: ProjectModel | None = None) -> ProjectModel:
        m = m or ProjectModel()
        m.id = e.id
        m.organization_id = e.organization_id
        m.team_id = e.team_id
        m.name = e.name
        m.key = e.key
        m.slug = str(e.slug)
        m.description = e.description
        m.start_date = e.start_date
        m.target_end_date = e.target_end_date
        m.is_archived = e.is_archived
        m.deleted_at = e.deleted_at
        return m


class SprintMapper:
    @staticmethod
    def to_entity(m: SprintModel) -> Sprint:
        return Sprint(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            project_id=m.project_id,
            name=m.name,
            goal=m.goal,
            start_date=m.start_date,
            end_date=m.end_date,
            status=SprintStatus(m.status),
            started_at=m.started_at,
            completed_at=m.completed_at,
            planned_capacity=m.planned_capacity,
            completed_points=m.completed_points,
        )

    @staticmethod
    def to_model(e: Sprint, m: SprintModel | None = None) -> SprintModel:
        m = m or SprintModel()
        m.id = e.id
        m.project_id = e.project_id
        m.name = e.name
        m.goal = e.goal
        m.start_date = e.start_date
        m.end_date = e.end_date
        m.status = e.status.value
        m.started_at = e.started_at
        m.completed_at = e.completed_at
        m.planned_capacity = e.planned_capacity
        m.completed_points = e.completed_points
        m.deleted_at = e.deleted_at
        return m


class WorkItemMapper:
    @staticmethod
    def to_entity(m: WorkItemModel) -> WorkItem:
        return WorkItem(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            project_id=m.project_id,
            sprint_id=m.sprint_id,
            parent_id=m.parent_id,
            epic_id=m.epic_id,
            external_key=m.external_key,
            title=m.title,
            description=m.description,
            item_type=WorkItemType(m.item_type),
            status=WorkItemStatus(m.status),
            priority=WorkItemPriority(m.priority),
            story_points=m.story_points,
            estimated_hours=m.estimated_hours,
            actual_hours=m.actual_hours,
            assignee_id=m.assignee_id,
            reporter_id=m.reporter_id,
            labels=list(m.labels or []),
            started_at=m.started_at,
            completed_at=m.completed_at,
        )

    @staticmethod
    def to_model(e: WorkItem, m: WorkItemModel | None = None) -> WorkItemModel:
        m = m or WorkItemModel()
        m.id = e.id
        m.project_id = e.project_id
        m.sprint_id = e.sprint_id
        m.parent_id = e.parent_id
        m.epic_id = e.epic_id
        m.external_key = e.external_key
        m.title = e.title
        m.description = e.description
        m.item_type = e.item_type.value
        m.status = e.status.value
        m.priority = e.priority.value
        m.story_points = e.story_points
        m.estimated_hours = e.estimated_hours
        m.actual_hours = e.actual_hours
        m.assignee_id = e.assignee_id
        m.reporter_id = e.reporter_id
        m.labels = list(e.labels)
        m.started_at = e.started_at
        m.completed_at = e.completed_at
        m.deleted_at = e.deleted_at
        return m


class BusinessOutcomeMapper:
    @staticmethod
    def to_entity(m: BusinessOutcomeModel) -> BusinessOutcome:
        return BusinessOutcome(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            organization_id=m.organization_id,
            owner_id=m.owner_id,
            name=m.name,
            description=m.description,
            hypothesis=m.hypothesis,
            status=OutcomeStatus(m.status),
            target_date=m.target_date,
            baseline_value=m.baseline_value,
            target_value=m.target_value,
            current_value=m.current_value,
            confidence_score=m.confidence_score,
            financial_impact_estimate=m.financial_impact_estimate,
        )

    @staticmethod
    def to_model(
        e: BusinessOutcome, m: BusinessOutcomeModel | None = None
    ) -> BusinessOutcomeModel:
        m = m or BusinessOutcomeModel()
        m.id = e.id
        m.organization_id = e.organization_id
        m.owner_id = e.owner_id
        m.name = e.name
        m.description = e.description
        m.hypothesis = e.hypothesis
        m.status = e.status.value
        m.target_date = e.target_date
        m.baseline_value = e.baseline_value
        m.target_value = e.target_value
        m.current_value = e.current_value
        m.confidence_score = e.confidence_score
        m.financial_impact_estimate = e.financial_impact_estimate
        m.deleted_at = e.deleted_at
        return m


class KPIMapper:
    @staticmethod
    def to_entity(m: KPIModel) -> KPI:
        return KPI(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            organization_id=m.organization_id,
            outcome_id=m.outcome_id,
            owner_id=m.owner_id,
            name=m.name,
            description=m.description,
            unit=KPIUnit(m.unit),
            currency=m.currency,
            direction=KPIDirection(m.direction),
            baseline_value=m.baseline_value,
            target_value=m.target_value,
            current_value=m.current_value,
            data_source=m.data_source,
            refresh_frequency_hours=m.refresh_frequency_hours,
            is_active=m.is_active,
        )

    @staticmethod
    def to_model(e: KPI, m: KPIModel | None = None) -> KPIModel:
        m = m or KPIModel()
        m.id = e.id
        m.organization_id = e.organization_id
        m.outcome_id = e.outcome_id
        m.owner_id = e.owner_id
        m.name = e.name
        m.description = e.description
        m.unit = e.unit.value
        m.currency = e.currency
        m.direction = e.direction.value
        m.baseline_value = e.baseline_value
        m.target_value = e.target_value
        m.current_value = e.current_value
        m.data_source = e.data_source
        m.refresh_frequency_hours = e.refresh_frequency_hours
        m.is_active = e.is_active
        m.deleted_at = e.deleted_at
        return m


class MetricSnapshotMapper:
    @staticmethod
    def to_entity(m: MetricSnapshotModel) -> MetricSnapshot:
        return MetricSnapshot(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            kpi_id=m.kpi_id,
            value=m.value,
            recorded_at=m.recorded_at,
            source=m.source,
            notes=m.notes,
            context=cast(dict, m.context or {}),
        )

    @staticmethod
    def to_model(
        e: MetricSnapshot, m: MetricSnapshotModel | None = None
    ) -> MetricSnapshotModel:
        m = m or MetricSnapshotModel()
        m.id = e.id
        m.kpi_id = e.kpi_id
        m.value = e.value
        m.recorded_at = e.recorded_at
        m.source = e.source
        m.notes = e.notes
        m.context = dict(e.context)
        m.deleted_at = e.deleted_at
        return m


class ObjectiveMapper:
    @staticmethod
    def to_entity(m: ObjectiveModel) -> Objective:
        return Objective(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            organization_id=m.organization_id,
            team_id=m.team_id,
            owner_id=m.owner_id,
            parent_id=m.parent_id,
            title=m.title,
            description=m.description,
            okr_type=OKRType(m.okr_type),
            status=OKRStatus(m.status),
            period_start=m.period_start,
            period_end=m.period_end,
        )

    @staticmethod
    def to_model(e: Objective, m: ObjectiveModel | None = None) -> ObjectiveModel:
        m = m or ObjectiveModel()
        m.id = e.id
        m.organization_id = e.organization_id
        m.team_id = e.team_id
        m.owner_id = e.owner_id
        m.parent_id = e.parent_id
        m.title = e.title
        m.description = e.description
        m.okr_type = e.okr_type.value
        m.status = e.status.value
        m.period_start = e.period_start
        m.period_end = e.period_end
        m.deleted_at = e.deleted_at
        return m


class KeyResultMapper:
    @staticmethod
    def to_entity(m: KeyResultModel) -> KeyResult:
        return KeyResult(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            objective_id=m.objective_id,
            kpi_id=m.kpi_id,
            title=m.title,
            description=m.description,
            baseline_value=m.baseline_value,
            target_value=m.target_value,
            current_value=m.current_value,
            weight=m.weight,
            status=OKRStatus(m.status),
        )

    @staticmethod
    def to_model(e: KeyResult, m: KeyResultModel | None = None) -> KeyResultModel:
        m = m or KeyResultModel()
        m.id = e.id
        m.objective_id = e.objective_id
        m.kpi_id = e.kpi_id
        m.title = e.title
        m.description = e.description
        m.baseline_value = Decimal(str(e.baseline_value))
        m.target_value = Decimal(str(e.target_value))
        m.current_value = Decimal(str(e.current_value))
        m.weight = Decimal(str(e.weight))
        m.status = e.status.value
        m.deleted_at = e.deleted_at
        return m


class AttributionMapper:
    @staticmethod
    def to_entity(m: OutcomeAttributionModel) -> OutcomeAttribution:
        return OutcomeAttribution(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            organization_id=m.organization_id,
            work_item_id=m.work_item_id,
            sprint_id=m.sprint_id,
            outcome_id=m.outcome_id,
            kpi_id=m.kpi_id,
            key_result_id=m.key_result_id,
            attributed_by_id=m.attributed_by_id,
            method=AttributionMethod(m.method),
            strength=AttributionStrength(m.strength),
            weight=m.weight,
            confidence=m.confidence,
            estimated_value=m.estimated_value,
            rationale=m.rationale,
        )

    @staticmethod
    def to_model(
        e: OutcomeAttribution, m: OutcomeAttributionModel | None = None
    ) -> OutcomeAttributionModel:
        m = m or OutcomeAttributionModel()
        m.id = e.id
        m.organization_id = e.organization_id
        m.work_item_id = e.work_item_id
        m.sprint_id = e.sprint_id
        m.outcome_id = e.outcome_id
        m.kpi_id = e.kpi_id
        m.key_result_id = e.key_result_id
        m.attributed_by_id = e.attributed_by_id
        m.method = e.method.value
        m.strength = e.strength.value
        m.weight = Decimal(str(e.weight))
        m.confidence = Decimal(str(e.confidence))
        m.estimated_value = e.estimated_value
        m.rationale = e.rationale
        m.deleted_at = e.deleted_at
        return m


class EvidenceMapper:
    @staticmethod
    def to_entity(m: EvidenceModel) -> Evidence:
        return Evidence(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
            attribution_id=m.attribution_id,
            author_id=m.author_id,
            title=m.title,
            content=m.content,
            source_url=m.source_url,
            evidence_type=m.evidence_type,
        )

    @staticmethod
    def to_model(e: Evidence, m: EvidenceModel | None = None) -> EvidenceModel:
        m = m or EvidenceModel()
        m.id = e.id
        m.attribution_id = e.attribution_id
        m.author_id = e.author_id
        m.title = e.title
        m.content = e.content
        m.source_url = e.source_url
        m.evidence_type = e.evidence_type
        m.deleted_at = e.deleted_at
        return m


class NotificationMapper:
    @staticmethod
    def to_entity(m: NotificationModel) -> Notification:
        return Notification(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            recipient_id=m.recipient_id,
            organization_id=m.organization_id,
            title=m.title,
            body=m.body,
            channel=NotificationChannel(m.channel),
            status=NotificationStatus(m.status),
            event_type=m.event_type,
            subject_type=m.subject_type,
            subject_id=m.subject_id,
            action_url=m.action_url,
            sent_at=m.sent_at,
            read_at=m.read_at,
            error_message=m.error_message,
        )

    @staticmethod
    def to_model(
        e: Notification, m: NotificationModel | None = None
    ) -> NotificationModel:
        m = m or NotificationModel()
        m.id = e.id
        m.recipient_id = e.recipient_id
        m.organization_id = e.organization_id
        m.title = e.title
        m.body = e.body
        m.channel = e.channel.value
        m.status = e.status.value
        m.event_type = e.event_type
        m.subject_type = e.subject_type
        m.subject_id = e.subject_id
        m.action_url = e.action_url
        m.sent_at = e.sent_at
        m.read_at = e.read_at
        m.error_message = e.error_message
        return m


class AuditLogMapper:
    @staticmethod
    def to_entity(m: AuditLogModel) -> AuditLog:
        return AuditLog(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            organization_id=m.organization_id,
            actor_id=m.actor_id,
            action=AuditAction(m.action),
            resource_type=m.resource_type,
            resource_id=m.resource_id,
            ip_address=m.ip_address,
            user_agent=m.user_agent,
            changes=cast(dict, m.changes or {}),
            metadata=cast(dict, m.audit_metadata or {}),
        )

    @staticmethod
    def to_model(e: AuditLog, m: AuditLogModel | None = None) -> AuditLogModel:
        m = m or AuditLogModel()
        m.id = e.id
        m.organization_id = e.organization_id
        m.actor_id = e.actor_id
        m.action = e.action.value
        m.resource_type = e.resource_type
        m.resource_id = e.resource_id
        m.ip_address = e.ip_address
        m.user_agent = e.user_agent
        m.changes = dict(e.changes)
        m.audit_metadata = dict(e.metadata)
        return m