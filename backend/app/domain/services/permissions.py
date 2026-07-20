"""Permission catalog and role → permission mapping."""

from __future__ import annotations

from enum import Enum

from app.core.exceptions import AuthorizationError
from app.domain.entities.user import User
from app.domain.enums import UserRole


class Permission(str, Enum):
    """Fine-grained permission catalog."""

    # Organizations
    ORG_READ = "org:read"
    ORG_MANAGE = "org:manage"

    # Users
    USER_READ = "user:read"
    USER_MANAGE = "user:manage"
    USER_INVITE = "user:invite"

    # Teams
    TEAM_READ = "team:read"
    TEAM_MANAGE = "team:manage"

    # Projects
    PROJECT_READ = "project:read"
    PROJECT_MANAGE = "project:manage"

    # Sprints
    SPRINT_READ = "sprint:read"
    SPRINT_MANAGE = "sprint:manage"

    # Work items
    WORK_ITEM_READ = "work_item:read"
    WORK_ITEM_WRITE = "work_item:write"

    # Outcomes
    OUTCOME_READ = "outcome:read"
    OUTCOME_MANAGE = "outcome:manage"

    # KPIs
    KPI_READ = "kpi:read"
    KPI_MANAGE = "kpi:manage"

    # OKRs
    OKR_READ = "okr:read"
    OKR_MANAGE = "okr:manage"

    # Attribution
    ATTRIBUTION_READ = "attribution:read"
    ATTRIBUTION_WRITE = "attribution:write"

    # Reports
    REPORT_READ = "report:read"

    # Audit
    AUDIT_READ = "audit:read"


_READ_ONLY: frozenset[Permission] = frozenset(
    {
        Permission.ORG_READ,
        Permission.USER_READ,
        Permission.TEAM_READ,
        Permission.PROJECT_READ,
        Permission.SPRINT_READ,
        Permission.WORK_ITEM_READ,
        Permission.OUTCOME_READ,
        Permission.KPI_READ,
        Permission.OKR_READ,
        Permission.ATTRIBUTION_READ,
        Permission.REPORT_READ,
    }
)

_ENGINEER: frozenset[Permission] = _READ_ONLY | frozenset(
    {
        Permission.WORK_ITEM_WRITE,
        Permission.ATTRIBUTION_WRITE,
    }
)

_MANAGER: frozenset[Permission] = _ENGINEER | frozenset(
    {
        Permission.TEAM_MANAGE,
        Permission.PROJECT_MANAGE,
        Permission.SPRINT_MANAGE,
        Permission.OUTCOME_MANAGE,
        Permission.KPI_MANAGE,
        Permission.OKR_MANAGE,
        Permission.USER_INVITE,
    }
)

_EXECUTIVE: frozenset[Permission] = _MANAGER | frozenset(
    {
        Permission.AUDIT_READ,
    }
)

_ORG_ADMIN: frozenset[Permission] = _EXECUTIVE | frozenset(
    {
        Permission.ORG_MANAGE,
        Permission.USER_MANAGE,
    }
)

_SUPER_ADMIN: frozenset[Permission] = frozenset(Permission)


_ROLE_PERMISSIONS: dict[UserRole, frozenset[Permission]] = {
    UserRole.SUPER_ADMIN: _SUPER_ADMIN,
    UserRole.ORG_ADMIN: _ORG_ADMIN,
    UserRole.EXECUTIVE: _EXECUTIVE,
    UserRole.PRODUCT_MANAGER: _MANAGER,
    UserRole.ENGINEERING_MANAGER: _MANAGER,
    UserRole.ENGINEER: _ENGINEER,
    UserRole.VIEWER: _READ_ONLY,
}


class PermissionRegistry:
    """Resolve and enforce permissions for users."""

    @staticmethod
    def permissions_for(role: UserRole) -> frozenset[Permission]:
        return _ROLE_PERMISSIONS.get(role, frozenset())

    @classmethod
    def has(cls, user: User, permission: Permission) -> bool:
        if not user.is_active:
            return False
        return permission in cls.permissions_for(user.role)

    @classmethod
    def has_any(cls, user: User, *permissions: Permission) -> bool:
        return any(cls.has(user, p) for p in permissions)

    @classmethod
    def has_all(cls, user: User, *permissions: Permission) -> bool:
        return all(cls.has(user, p) for p in permissions)

    @classmethod
    def ensure(cls, user: User, permission: Permission) -> None:
        if not cls.has(user, permission):
            raise AuthorizationError(
                f"Missing required permission: {permission.value}"
            )

    @classmethod
    def ensure_any(cls, user: User, *permissions: Permission) -> None:
        if not cls.has_any(user, *permissions):
            required = ", ".join(p.value for p in permissions)
            raise AuthorizationError(
                f"Requires at least one of the following permissions: {required}"
            )