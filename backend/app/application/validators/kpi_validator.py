"""Cross-aggregate validators for KPI operations."""

from __future__ import annotations

from uuid import UUID

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class KPIValidator:
    """Validate KPI preconditions using the current unit of work."""

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
            raise ValidationError("KPI name is required")
        if self._uow.kpis.name_exists(organization_id, name.strip(), exclude_id):
            raise ConflictError(
                f"A KPI named '{name.strip()}' already exists in this organization"
            )

    def ensure_owner_in_org(
        self, owner_id: UUID | None, organization_id: UUID
    ) -> None:
        """Ensure the owner belongs to the organization."""
        if owner_id is None:
            return
        user = self._uow.users.get_by_id(owner_id)
        if user is None:
            raise NotFoundError(f"User {owner_id} not found")
        if not user.is_active:
            raise ValidationError("Owner must be an active user")
        if user.organization_id != organization_id:
            raise ValidationError("Owner must belong to your organization")

    def ensure_outcome_in_org(
        self, outcome_id: UUID | None, organization_id: UUID
    ) -> None:
        """Ensure the linked business outcome belongs to the organization."""
        if outcome_id is None:
            return
        outcome = self._uow.outcomes.get_by_id(outcome_id)
        if outcome is None:
            raise NotFoundError(f"Business outcome {outcome_id} not found")
        if outcome.organization_id != organization_id:
            raise ValidationError(
                "Business outcome must belong to your organization"
            )

    def ensure_deletable(self, kpi_id: UUID) -> None:
        """Prevent deletion when KPI history exists."""
        latest = self._uow.metric_snapshots.latest_for_kpi(kpi_id)
        if latest is not None:
            raise ValidationError(
                "Cannot delete a KPI that has historical snapshots; "
                "deactivate it instead"
            )
        attributions = self._uow.attributions.list_by_kpi(kpi_id)
        if attributions:
            raise ValidationError(
                "Cannot delete a KPI that has attributions; "
                "deactivate it or remove attributions first"
            )