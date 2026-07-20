"""Domain enumerations."""

from enum import Enum


class UserRole(str, Enum):
    """System-wide user roles."""

    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    EXECUTIVE = "executive"
    PRODUCT_MANAGER = "product_manager"
    ENGINEERING_MANAGER = "engineering_manager"
    ENGINEER = "engineer"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """User account status."""

    ACTIVE = "active"
    INVITED = "invited"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class SprintStatus(str, Enum):
    """Sprint lifecycle status."""

    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WorkItemType(str, Enum):
    """Type of work item."""

    EPIC = "epic"
    STORY = "story"
    TASK = "task"
    BUG = "bug"
    SPIKE = "spike"


class WorkItemStatus(str, Enum):
    """Work item status."""

    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"


class WorkItemPriority(str, Enum):
    """Work item priority."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class OutcomeStatus(str, Enum):
    """Business outcome status."""

    PROPOSED = "proposed"
    ACTIVE = "active"
    ACHIEVED = "achieved"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"
    ABANDONED = "abandoned"


class KPIDirection(str, Enum):
    """Desired direction of a KPI."""

    INCREASE = "increase"
    DECREASE = "decrease"
    MAINTAIN = "maintain"


class KPIUnit(str, Enum):
    """Common KPI units."""

    CURRENCY = "currency"
    PERCENT = "percent"
    COUNT = "count"
    RATIO = "ratio"
    DURATION_SECONDS = "duration_seconds"
    DURATION_DAYS = "duration_days"
    SCORE = "score"


class OKRStatus(str, Enum):
    """OKR status."""

    DRAFT = "draft"
    ACTIVE = "active"
    ACHIEVED = "achieved"
    MISSED = "missed"
    CANCELLED = "cancelled"


class OKRType(str, Enum):
    """Level of the OKR."""

    COMPANY = "company"
    TEAM = "team"
    INDIVIDUAL = "individual"


class AttributionMethod(str, Enum):
    """How an attribution was determined."""

    MANUAL = "manual"
    INFERRED = "inferred"
    STATISTICAL = "statistical"


class AttributionStrength(str, Enum):
    """Confidence level of an attribution."""

    PRIMARY = "primary"
    CONTRIBUTING = "contributing"
    SUPPORTING = "supporting"
    NONE = "none"


class NotificationChannel(str, Enum):
    """Notification delivery channels."""

    IN_APP = "in_app"
    EMAIL = "email"
    WEBHOOK = "webhook"


class NotificationStatus(str, Enum):
    """Notification lifecycle status."""

    PENDING = "pending"
    SENT = "sent"
    READ = "read"
    FAILED = "failed"


class AuditAction(str, Enum):
    """Audit log actions."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    INVITE = "invite"
    PERMISSION_CHANGE = "permission_change"