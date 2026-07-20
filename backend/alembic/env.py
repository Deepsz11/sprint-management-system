"""Alembic environment configuration."""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.infrastructure.persistence.models import Base  # noqa: F401
from app.infrastructure.persistence.models.attribution import (  # noqa: F401
    EvidenceModel,
    OutcomeAttributionModel,
)
from app.infrastructure.persistence.models.audit_log import AuditLogModel  # noqa: F401
from app.infrastructure.persistence.models.business_outcome import (  # noqa: F401
    BusinessOutcomeModel,
)
from app.infrastructure.persistence.models.kpi import (  # noqa: F401
    KPIModel,
    MetricSnapshotModel,
)
from app.infrastructure.persistence.models.notification import (  # noqa: F401
    NotificationModel,
)
from app.infrastructure.persistence.models.okr import (  # noqa: F401
    KeyResultModel,
    ObjectiveModel,
)
from app.infrastructure.persistence.models.organization import (  # noqa: F401
    OrganizationModel,
    TeamModel,
)
from app.infrastructure.persistence.models.project import ProjectModel  # noqa: F401
from app.infrastructure.persistence.models.session import UserSessionModel  # noqa: F401
from app.infrastructure.persistence.models.sprint import SprintModel  # noqa: F401
from app.infrastructure.persistence.models.user import (  # noqa: F401
    TeamMembershipModel,
    UserModel,
)
from app.infrastructure.persistence.models.work_item import WorkItemModel  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = settings.database_url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()