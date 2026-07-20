"""Entity → DTO mappers for the application layer."""

from __future__ import annotations

from app.application.dtos.attribution import AttributionDTO, EvidenceDTO
from app.application.dtos.kpi import KPIDTO, MetricSnapshotDTO
from app.application.dtos.notification import NotificationDTO
from app.application.dtos.okr import KeyResultDTO, ObjectiveDTO
from app.application.dtos.organization import OrganizationDTO, TeamDTO
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.dtos.project import ProjectDTO
from app.application.dtos.sprint import SprintDTO
from app.application.dtos.user import UserDTO
from app.application.dtos.work_item import WorkItemDTO
from app.domain.entities.attribution import Evidence, OutcomeAttribution
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.entities.kpi import KPI, MetricSnapshot
from app.domain.entities.notification import Notification
from app.domain.entities.okr import KeyResult, Objective
from app.domain.entities.organization import Organization, Team
from app.domain.entities.project import Project
from app.domain.entities.sprint import Sprint
from app.domain.entities.user import User
from app.domain.entities.work_item import WorkItem


def organization_to_dto(e: Organization) -> OrganizationDTO:
    return OrganizationDTO(
        id=e.id,
        name=e.name,
        slug=str(e.slug),
        description=e.description,
        billing_email=e.billing_email,
        is_active=e.is_active,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def team_to_dto(e: Team) -> TeamDTO:
    return TeamDTO(
        id=e.id,
        organization_id=e.organization_id,
        name=e.name,
        slug=str(e.slug),
        description=e.description,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def user_to_dto(e: User) -> UserDTO:
    return UserDTO(
        id=e.id,
        email=str(e.email),
        full_name=e.full_name,
        organization_id=e.organization_id,
        role=e.role,
        status=e.status,
        last_login_at=e.last_login_at,
        is_email_verified=e.is_email_verified,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def project_to_dto(e: Project) -> ProjectDTO:
    return ProjectDTO(
        id=e.id,
        organization_id=e.organization_id,
        team_id=e.team_id,
        name=e.name,
        key=e.key,
        slug=str(e.slug),
        description=e.description,
        start_date=e.start_date,
        target_end_date=e.target_end_date,
        is_archived=e.is_archived,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def sprint_to_dto(e: Sprint) -> SprintDTO:
    return SprintDTO(
        id=e.id,
        project_id=e.project_id,
        name=e.name,
        goal=e.goal,
        start_date=e.start_date,
        end_date=e.end_date,
        status=e.status,
        started_at=e.started_at,
        completed_at=e.completed_at,
        planned_capacity=e.planned_capacity,
        completed_points=e.completed_points,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def work_item_to_dto(e: WorkItem) -> WorkItemDTO:
    return WorkItemDTO(
        id=e.id,
        project_id=e.project_id,
        sprint_id=e.sprint_id,
        parent_id=e.parent_id,
        epic_id=e.epic_id,
        external_key=e.external_key,
        title=e.title,
        description=e.description,
        item_type=e.item_type,
        status=e.status,
        priority=e.priority,
        story_points=e.story_points,
        estimated_hours=e.estimated_hours,
        actual_hours=e.actual_hours,
        assignee_id=e.assignee_id,
        reporter_id=e.reporter_id,
        labels=list(e.labels),
        started_at=e.started_at,
        completed_at=e.completed_at,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def outcome_to_dto(e: BusinessOutcome) -> BusinessOutcomeDTO:
    return BusinessOutcomeDTO(
        id=e.id,
        organization_id=e.organization_id,
        owner_id=e.owner_id,
        name=e.name,
        description=e.description,
        hypothesis=e.hypothesis,
        status=e.status,
        target_date=e.target_date,
        baseline_value=e.baseline_value,
        target_value=e.target_value,
        current_value=e.current_value,
        progress_percent=e.progress_percent,
        confidence_score=e.confidence_score,
        financial_impact_estimate=e.financial_impact_estimate,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def kpi_to_dto(e: KPI) -> KPIDTO:
    return KPIDTO(
        id=e.id,
        organization_id=e.organization_id,
        outcome_id=e.outcome_id,
        owner_id=e.owner_id,
        name=e.name,
        description=e.description,
        unit=e.unit,
        currency=e.currency,
        direction=e.direction,
        baseline_value=e.baseline_value,
        target_value=e.target_value,
        current_value=e.current_value,
        data_source=e.data_source,
        refresh_frequency_hours=e.refresh_frequency_hours,
        is_active=e.is_active,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def metric_snapshot_to_dto(e: MetricSnapshot) -> MetricSnapshotDTO:
    return MetricSnapshotDTO(
        id=e.id,
        kpi_id=e.kpi_id,
        value=e.value,
        recorded_at=e.recorded_at,
        source=e.source,
        notes=e.notes,
        context=dict(e.context),
        created_at=e.created_at,
    )


def objective_to_dto(e: Objective) -> ObjectiveDTO:
    return ObjectiveDTO(
        id=e.id,
        organization_id=e.organization_id,
        team_id=e.team_id,
        owner_id=e.owner_id,
        parent_id=e.parent_id,
        title=e.title,
        description=e.description,
        okr_type=e.okr_type,
        status=e.status,
        period_start=e.period_start,
        period_end=e.period_end,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def key_result_to_dto(e: KeyResult) -> KeyResultDTO:
    return KeyResultDTO(
        id=e.id,
        objective_id=e.objective_id,
        kpi_id=e.kpi_id,
        title=e.title,
        description=e.description,
        baseline_value=e.baseline_value,
        target_value=e.target_value,
        current_value=e.current_value,
        progress_percent=e.progress_percent,
        weight=e.weight,
        status=e.status,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def attribution_to_dto(e: OutcomeAttribution) -> AttributionDTO:
    return AttributionDTO(
        id=e.id,
        organization_id=e.organization_id,
        work_item_id=e.work_item_id,
        sprint_id=e.sprint_id,
        outcome_id=e.outcome_id,
        kpi_id=e.kpi_id,
        key_result_id=e.key_result_id,
        attributed_by_id=e.attributed_by_id,
        method=e.method,
        strength=e.strength,
        weight=e.weight,
        confidence=e.confidence,
        estimated_value=e.estimated_value,
        rationale=e.rationale,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def evidence_to_dto(e: Evidence) -> EvidenceDTO:
    return EvidenceDTO(
        id=e.id,
        attribution_id=e.attribution_id,
        author_id=e.author_id,
        title=e.title,
        content=e.content,
        source_url=e.source_url,
        evidence_type=e.evidence_type,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


def notification_to_dto(e: Notification) -> NotificationDTO:
    return NotificationDTO(
        id=e.id,
        recipient_id=e.recipient_id,
        organization_id=e.organization_id,
        title=e.title,
        body=e.body,
        channel=e.channel,
        status=e.status,
        event_type=e.event_type,
        subject_type=e.subject_type,
        subject_id=e.subject_id,
        action_url=e.action_url,
        sent_at=e.sent_at,
        read_at=e.read_at,
        created_at=e.created_at,
    )