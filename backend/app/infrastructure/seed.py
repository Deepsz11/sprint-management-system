"""Seed data for local development and initial deployments."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from app.core.logging import get_logger
from app.core.security import hash_password
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.entities.kpi import KPI
from app.domain.entities.organization import Organization, Team
from app.domain.entities.project import Project
from app.domain.entities.sprint import Sprint
from app.domain.entities.user import User
from app.domain.enums import (
    KPIDirection,
    KPIUnit,
    OutcomeStatus,
    SprintStatus,
    UserRole,
    UserStatus,
)
from app.domain.value_objects import Email, Slug
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

_logger = get_logger("infrastructure.seed")

DEFAULT_ADMIN_EMAIL = "admin@sbot.local"
DEFAULT_ADMIN_PASSWORD = "ChangeMe123!"
DEFAULT_ORG_SLUG = "acme"


def seed_default_data(
    admin_email: str = DEFAULT_ADMIN_EMAIL,
    admin_password: str = DEFAULT_ADMIN_PASSWORD,
    organization_slug: str = DEFAULT_ORG_SLUG,
) -> None:
    """Idempotently seed a default organization, admin user, project and sprint."""
    with SQLAlchemyUnitOfWork() as uow:
        organization = uow.organizations.get_by_slug(organization_slug)
        if organization is None:
            organization = uow.organizations.add(
                Organization(
                    name="Acme Corporation",
                    slug=Slug(organization_slug),
                    description="Default seeded organization",
                    billing_email="billing@acme.local",
                    is_active=True,
                )
            )
            _logger.info("Seeded organization: %s", organization.name)

        admin = uow.users.get_by_email(admin_email)
        if admin is None:
            admin = uow.users.add(
                User(
                    email=Email(admin_email),
                    hashed_password=hash_password(admin_password),
                    full_name="Platform Administrator",
                    organization_id=organization.id,
                    role=UserRole.ORG_ADMIN,
                    status=UserStatus.ACTIVE,
                    is_email_verified=True,
                )
            )
            _logger.info("Seeded admin user: %s", admin.email)

        team = uow.teams.get_by_slug(organization.id, "core-platform")
        if team is None:
            team = uow.teams.add(
                Team(
                    organization_id=organization.id,
                    name="Core Platform",
                    slug=Slug("core-platform"),
                    description="Default engineering team",
                )
            )
            _logger.info("Seeded team: %s", team.name)

        project = uow.projects.get_by_key(organization.id, "SBOT")
        if project is None:
            today = date.today()
            project = uow.projects.add(
                Project(
                    organization_id=organization.id,
                    team_id=team.id,
                    name="Sprint Outcome Tracer",
                    key="SBOT",
                    slug=Slug("sprint-outcome-tracer"),
                    description="Default seeded project for evaluation",
                    start_date=today,
                    target_end_date=today + timedelta(days=180),
                )
            )
            _logger.info("Seeded project: %s", project.name)

            uow.sprints.add(
                Sprint(
                    project_id=project.id,
                    name="Sprint 1",
                    goal="Establish baseline metrics and delivery cadence",
                    start_date=today,
                    end_date=today + timedelta(days=13),
                    status=SprintStatus.PLANNED,
                    planned_capacity=40,
                )
            )
            _logger.info("Seeded initial sprint for project %s", project.key)

        outcome = None
        outcomes = uow.outcomes.list_by_organization(
            organization.id,
            page=_default_page(),
        )
        if not outcomes:
            outcome = uow.outcomes.add(
                BusinessOutcome(
                    organization_id=organization.id,
                    owner_id=admin.id,
                    name="Increase Monthly Active Users",
                    description="Grow MAU by 20% within two quarters",
                    hypothesis=(
                        "Improved onboarding and dashboards will accelerate adoption"
                    ),
                    status=OutcomeStatus.ACTIVE,
                    target_date=date.today() + timedelta(days=180),
                    baseline_value=Decimal("10000"),
                    target_value=Decimal("12000"),
                    current_value=Decimal("10000"),
                    confidence_score=Decimal("70"),
                    financial_impact_estimate=Decimal("250000"),
                )
            )
            _logger.info("Seeded outcome: %s", outcome.name)

        kpis = uow.kpis.list_by_organization(organization.id, page=_default_page())
        if not kpis:
            uow.kpis.add(
                KPI(
                    organization_id=organization.id,
                    outcome_id=outcome.id if outcome else None,
                    owner_id=admin.id,
                    name="Monthly Active Users",
                    description="Distinct users active over trailing 30 days",
                    unit=KPIUnit.COUNT,
                    direction=KPIDirection.INCREASE,
                    baseline_value=Decimal("10000"),
                    target_value=Decimal("12000"),
                    current_value=Decimal("10000"),
                    data_source="analytics.mau_daily",
                    refresh_frequency_hours=24,
                    is_active=True,
                )
            )
            _logger.info("Seeded default KPI: Monthly Active Users")

        uow.commit()


def _default_page():
    from app.domain.repositories.specifications import PageRequest

    return PageRequest(limit=1, offset=0)