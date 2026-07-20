"""Domain repository contracts."""

from app.domain.repositories.base import Repository, UnitOfWork
from app.domain.repositories.interfaces import (
    AttributionRepository,
    AuditLogRepository,
    BusinessOutcomeRepository,
    EvidenceRepository,
    KPIRepository,
    KeyResultRepository,
    MetricSnapshotRepository,
    NotificationRepository,
    ObjectiveRepository,
    OrganizationRepository,
    ProjectRepository,
    SprintRepository,
    TeamMembershipRepository,
    TeamRepository,
    UserRepository,
    WorkItemRepository,
)

__all__ = [
    "Repository",
    "UnitOfWork",
    "AttributionRepository",
    "AuditLogRepository",
    "BusinessOutcomeRepository",
    "EvidenceRepository",
    "KPIRepository",
    "KeyResultRepository",
    "MetricSnapshotRepository",
    "NotificationRepository",
    "ObjectiveRepository",
    "OrganizationRepository",
    "ProjectRepository",
    "SprintRepository",
    "TeamMembershipRepository",
    "TeamRepository",
    "UserRepository",
    "WorkItemRepository",
]