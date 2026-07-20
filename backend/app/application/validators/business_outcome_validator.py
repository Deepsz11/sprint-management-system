"""Cross-aggregate validators for business outcome operations."""

from __future__ import annotations

from uuid import UUID

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class BusinessOutcomeValidator:
    """Validate outcome preconditions using the current unit of work."""

    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self._uow = uow

    def ensure_unique_name(
        self,
        organization_id: UUID,
        name: str,
        exclude_id: UUID | None = None,
    ) -> None:
        """Enforce name uniqueness within an organization."""
        if not name or not name.strip():
            raise ValidationError("Outcome name is required")
        if self._uow.outcomes.name_exists(organization_id, name.strip(), exclude_id):
            raise ConflictError(
                f"An outcome named '{name.strip()}' already exists in this organization"
            )

    def ensure_owner_in_org(
        self,
        owner_id: UUID | None,
        organization_id: UUID,
    ) -> None:
        """Ensure the proposed owner belongs to the organization."""
        if owner_id is None:
            return
        user = self._uow.users.get_by_id(owner_id)
        if user is None:
            raise NotFoundError(f"User {owner_id} not found")
        if not user.is_active:
            raise ValidationError("Owner must be an active user")
        if user.organization_id != organization_id:
            raise ValidationError("Owner must belong to your organization")

    def ensure_deletable(self, outcome_id: UUID) -> None:
        """Prevent deletion when historical KPI data exists for the outcome."""
        kpis = self._uow.kpis.list_by_outcome(outcome_id)
        if not kpis:
            return
        for kpi in kpis:
            snapshot = self._uow.metric_snapshots.latest_for_kpi(kpi.id)
            if snapshot is not None:
                raise ValidationError(
                    "Cannot delete an outcome that has historical KPI data; "
                    "archive it instead"
                )