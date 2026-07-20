"""Domain service enforcing role-based access control."""

from __future__ import annotations

from uuid import UUID

from app.core.exceptions import AuthorizationError
from app.domain.entities.user import User
from app.domain.enums import UserRole


class AuthorizationDomainService:
    """Central authorization rules for the domain."""

    _ADMIN_ROLES = {UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN}
    _MANAGER_ROLES = _ADMIN_ROLES | {
        UserRole.PRODUCT_MANAGER,
        UserRole.ENGINEERING_MANAGER,
        UserRole.EXECUTIVE,
    }
    _EDITOR_ROLES = _MANAGER_ROLES | {UserRole.ENGINEER}

    @classmethod
    def ensure_same_organization(
        cls, user: User, organization_id: UUID | None
    ) -> None:
        if user.role == UserRole.SUPER_ADMIN:
            return
        if user.organization_id is None or user.organization_id != organization_id:
            raise AuthorizationError("Cross-organization access is not permitted")

    @classmethod
    def can_manage_organization(cls, user: User) -> bool:
        return user.role in cls._ADMIN_ROLES

    @classmethod
    def can_manage_users(cls, user: User) -> bool:
        return user.role in cls._ADMIN_ROLES

    @classmethod
    def can_manage_outcomes(cls, user: User) -> bool:
        return user.role in cls._MANAGER_ROLES

    @classmethod
    def can_manage_okrs(cls, user: User) -> bool:
        return user.role in cls._MANAGER_ROLES

    @classmethod
    def can_manage_kpis(cls, user: User) -> bool:
        return user.role in cls._MANAGER_ROLES

    @classmethod
    def can_manage_projects(cls, user: User) -> bool:
        return user.role in cls._MANAGER_ROLES

    @classmethod
    def can_manage_sprints(cls, user: User) -> bool:
        return user.role in cls._MANAGER_ROLES

    @classmethod
    def can_edit_work_items(cls, user: User) -> bool:
        return user.role in cls._EDITOR_ROLES

    @classmethod
    def can_create_attribution(cls, user: User) -> bool:
        return user.role in cls._EDITOR_ROLES

    @classmethod
    def can_view(cls, user: User) -> bool:
        return user.is_active

    @classmethod
    def ensure(cls, permitted: bool, message: str) -> None:
        if not permitted:
            raise AuthorizationError(message)