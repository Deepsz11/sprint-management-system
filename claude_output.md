### test/hello.py

```python
print("Hello from Python")
```

### test/readme.md

```markdown
# This file was created automatically
```

================================================================================

### test/hello.py

```python
print("Hello from Python")
```

### test/readme.md

```markdown
# This file was created automatically
```

================================================================================

I notice you've shared a file (`test/hello.py`) that doesn't relate to the **Sprint Business Outcome Tracer** application I'm building.

To stay aligned with the product, I need to confirm a few things before proceeding:

### Questions for You

1. **Purpose of this file** — Is `test/hello.py` meant to be:
   - A smoke test scaffold for the project's test suite?
   - Something to ignore/discard?
   - A hint that the backend should be Python (e.g., FastAPI)?

2. **Tech Stack Confirmation** — Since I haven't been given the stack yet, please confirm:
   - **Backend language/framework**: Python (FastAPI / Django) or something else?
   - **Frontend**: React / Vue / Server-rendered?
   - **Database**: PostgreSQL / SQLite / other?
   - **Testing framework**: pytest / unittest?

3. **Sprint Business Outcome Tracer — Core Requirements** — Before writing any code, I need to nail down the domain. My working understanding is:
   > *An application that links sprint-level work items to measurable business outcomes (KPIs, OKRs, revenue impact), so teams can trace which sprints delivered which business value.*
   
   Please confirm or correct these core concepts:
   - **Sprint**: Time-boxed iteration with start/end dates, goals, and committed work items.
   - **Work Item**: A unit of delivered work within a sprint (feature, story, epic).
   - **Business Outcome**: A measurable business result (e.g., "Reduce churn by 5%", "Increase MRR by $10K").
   - **Trace Link**: The relationship connecting a Work Item → Outcome, with attribution weight and evidence.
   - **Metric Snapshot**: Time-series data points showing outcome progress.

4. **Primary Users & Use Cases** — Who uses this?
   - Product Managers tracing feature → KPI impact?
   - Engineering Leaders reporting sprint ROI to executives?
   - Both?

5. **Scope of MVP** — What's in the first release?
   - Manual outcome/sprint entry?
   - Integrations (Jira, Linear, GitHub)?
   - Reporting/dashboards?

Once you confirm the stack and core domain, I'll produce the clean-architecture project skeleton (domain → use cases → interface adapters → frameworks) and real, production-ready code — no placeholders.

**Please answer the questions above so I can proceed correctly.**

================================================================================

### test/hello.py

```python
print("Hello from Python")
```

### test/readme.md

```markdown
# Auto generated
```

================================================================================

### test/hello.py

```python
print("Hello from Python")
```

### test/readme.md

```markdown
# Auto generated
```

================================================================================

### test/hello.py

```python
print("Hello from Python")
```

### test/readme.md

```markdown
# Auto generated
```

================================================================================

### test/hello.py

```python
print("Hello from Python")
```

================================================================================

### test/hello.py

```python
print("Hello from Python")
```

================================================================================

### test/hello.py

```python
print("Hello from Python")
```

### test/readme.md

```markdown
# Auto generated
```

================================================================================

### backend/pyproject.toml

```toml
[tool.poetry]
name = "sprint-outcome-tracer"
version = "0.1.0"
description = "Sprint Business Outcome Tracer - Trace engineering work to measurable business outcomes"
authors = ["Engineering Team"]
readme = "README.md"
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
sqlalchemy = "^2.0.25"
alembic = "^1.13.1"
psycopg2-binary = "^2.9.9"
pydantic = "^2.5.3"
pydantic-settings = "^2.1.0"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-multipart = "^0.0.6"
email-validator = "^2.1.0"
python-dateutil = "^2.8.2"
httpx = "^0.26.0"
redis = "^5.0.1"
celery = "^5.3.6"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.4"
pytest-asyncio = "^0.23.3"
pytest-cov = "^4.1.0"
black = "^23.12.1"
ruff = "^0.1.14"
mypy = "^1.8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W", "B", "C4", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

### backend/app/__init__.py

```python
"""Sprint Business Outcome Tracer - Backend Application."""

__version__ = "0.1.0"
```

### backend/app/core/config.py

```python
"""Application configuration management."""

from functools import lru_cache
from typing import List

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Sprint Business Outcome Tracer"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PASSWORD_MIN_LENGTH: int = 8

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "sbot"
    POSTGRES_PASSWORD: str = "sbot"
    POSTGRES_DB: str = "sbot"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def database_url(self) -> str:
        """Construct SQLAlchemy database URL."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def database_url_async(self) -> str:
        """Construct SQLAlchemy async database URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()
```

### backend/app/core/exceptions.py

```python
"""Domain and application exceptions."""

from typing import Any


class ApplicationError(Exception):
    """Base class for all application exceptions."""

    default_message: str = "An application error occurred"
    status_code: int = 500

    def __init__(self, message: str | None = None, details: dict[str, Any] | None = None):
        self.message = message or self.default_message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(ApplicationError):
    """Raised when a requested resource cannot be found."""

    default_message = "Resource not found"
    status_code = 404


class ConflictError(ApplicationError):
    """Raised when a resource conflicts with existing state."""

    default_message = "Resource conflict"
    status_code = 409


class ValidationError(ApplicationError):
    """Raised when input validation fails at the domain level."""

    default_message = "Validation failed"
    status_code = 422


class AuthenticationError(ApplicationError):
    """Raised when authentication fails."""

    default_message = "Authentication failed"
    status_code = 401


class AuthorizationError(ApplicationError):
    """Raised when a user lacks permission to perform an action."""

    default_message = "Not authorized"
    status_code = 403


class BusinessRuleViolationError(ApplicationError):
    """Raised when a business rule is violated."""

    default_message = "Business rule violation"
    status_code = 422


class ExternalServiceError(ApplicationError):
    """Raised when an external service call fails."""

    default_message = "External service error"
    status_code = 502
```

### backend/app/core/security.py

```python
"""Security primitives: password hashing and JWT tokens."""

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import AuthenticationError

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return _pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str | UUID,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed JWT access token."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    if additional_claims:
        to_encode.update(additional_claims)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str | UUID) -> str:
    """Create a signed JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as exc:
        raise AuthenticationError("Invalid or expired token") from exc
```

### backend/app/core/logging.py

```python
"""Centralized structured logging configuration."""

import logging
import sys
from logging.config import dictConfig

from app.core.config import settings


def configure_logging() -> None:
    """Configure application-wide logging."""
    log_level = "DEBUG" if settings.DEBUG else "INFO"

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": (
                        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
                    ),
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                    "level": log_level,
                },
            },
            "loggers": {
                "app": {"handlers": ["console"], "level": log_level, "propagate": False},
                "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
                "uvicorn.error": {"handlers": ["console"], "level": "INFO", "propagate": False},
                "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
                "sqlalchemy.engine": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
            "root": {"handlers": ["console"], "level": log_level},
        }
    )


def get_logger(name: str) -> logging.Logger:
    """Return an application logger."""
    return logging.getLogger(f"app.{name}")
```

### backend/app/domain/__init__.py

```python
"""Domain layer - pure business logic, no external dependencies."""
```

### backend/app/domain/enums.py

```python
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
```

### backend/app/domain/value_objects.py

```python
"""Domain value objects - immutable primitives with validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal

from app.core.exceptions import ValidationError

_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
_SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class Email:
    """A validated email address."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not _EMAIL_REGEX.match(normalized):
            raise ValidationError(f"Invalid email address: {self.value}")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Slug:
    """A URL-safe slug identifier."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not _SLUG_REGEX.match(normalized):
            raise ValidationError(
                f"Invalid slug: {self.value}. Must be lowercase alphanumeric with hyphens."
            )
        if len(normalized) > 64:
            raise ValidationError("Slug must be 64 characters or fewer")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DateRange:
    """An inclusive date range with a start and end."""

    start: date
    end: date

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValidationError("End date cannot be before start date")

    def contains(self, target: date) -> bool:
        return self.start <= target <= self.end

    def overlaps(self, other: DateRange) -> bool:
        return not (self.end < other.start or other.end < self.start)

    @property
    def duration_days(self) -> int:
        return (self.end - self.start).days + 1


@dataclass(frozen=True, slots=True)
class MonetaryAmount:
    """A monetary amount with currency."""

    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        currency = self.currency.strip().upper()
        if len(currency) != 3 or not currency.isalpha():
            raise ValidationError(f"Invalid currency code: {self.currency}")
        object.__setattr__(self, "currency", currency)

    def __add__(self, other: MonetaryAmount) -> MonetaryAmount:
        if self.currency != other.currency:
            raise ValidationError("Cannot add amounts with different currencies")
        return MonetaryAmount(self.amount + other.amount, self.currency)


@dataclass(frozen=True, slots=True)
class MetricValue:
    """A recorded metric value at a point in time."""

    value: Decimal
    recorded_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, "value", Decimal(str(self.value)))
        if self.recorded_at.tzinfo is None:
            object.__setattr__(
                self, "recorded_at", self.recorded_at.replace(tzinfo=timezone.utc)
            )


@dataclass(frozen=True, slots=True)
class Percentage:
    """A percentage value between 0 and 100."""

    value: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, "value", Decimal(str(self.value)))
        if self.value < Decimal("0") or self.value > Decimal("100"):
            raise ValidationError(f"Percentage must be between 0 and 100, got {self.value}")

    def as_ratio(self) -> Decimal:
        return self.value / Decimal("100")
```

### backend/app/domain/entities/base.py

```python
"""Base entity types shared across the domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class Entity:
    """Base class for all domain entities."""

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        """Update the entity's updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)


@dataclass
class SoftDeletableEntity(Entity):
    """An entity that supports soft deletion."""

    deleted_at: datetime | None = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        if self.deleted_at is None:
            self.deleted_at = datetime.now(timezone.utc)
            self.touch()

    def restore(self) -> None:
        if self.deleted_at is not None:
            self.deleted_at = None
            self.touch()
```

### backend/app/domain/entities/__init__.py

```python
"""Domain entities."""

from app.domain.entities.base import Entity, SoftDeletableEntity

__all__ = ["Entity", "SoftDeletableEntity"]
```

### backend/app/domain/entities/organization.py

```python
"""Organization aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.value_objects import Slug


@dataclass
class Organization(SoftDeletableEntity):
    """A tenant organization within the multi-tenant system."""

    name: str = ""
    slug: Slug = field(default_factory=lambda: Slug("default"))
    description: str | None = None
    billing_email: str | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Organization name is required")
        if len(self.name) > 200:
            raise ValidationError("Organization name must be 200 characters or fewer")

    def rename(self, new_name: str) -> None:
        if not new_name or not new_name.strip():
            raise ValidationError("Organization name is required")
        self.name = new_name.strip()
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()

    def activate(self) -> None:
        self.is_active = True
        self.touch()


@dataclass
class Team(SoftDeletableEntity):
    """A team within an organization."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    name: str = ""
    slug: Slug = field(default_factory=lambda: Slug("default"))
    description: str | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Team name is required")
        if self.organization_id == UUID(int=0):
            raise ValidationError("Team must belong to an organization")

    def rename(self, new_name: str) -> None:
        if not new_name or not new_name.strip():
            raise ValidationError("Team name is required")
        self.name = new_name.strip()
        self.touch()
```

### backend/app/domain/entities/user.py

```python
"""User aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import UserRole, UserStatus
from app.domain.value_objects import Email


@dataclass
class User(SoftDeletableEntity):
    """A user of the system."""

    email: Email = field(default_factory=lambda: Email("user@example.com"))
    hashed_password: str = ""
    full_name: str = ""
    organization_id: UUID | None = None
    role: UserRole = UserRole.VIEWER
    status: UserStatus = UserStatus.INVITED
    last_login_at: datetime | None = None
    is_email_verified: bool = False

    def __post_init__(self) -> None:
        if not self.full_name or not self.full_name.strip():
            raise ValidationError("Full name is required")
        if len(self.full_name) > 200:
            raise ValidationError("Full name must be 200 characters or fewer")

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE and not self.is_deleted

    def activate(self) -> None:
        self.status = UserStatus.ACTIVE
        self.touch()

    def suspend(self) -> None:
        self.status = UserStatus.SUSPENDED
        self.touch()

    def deactivate(self) -> None:
        self.status = UserStatus.DEACTIVATED
        self.touch()

    def record_login(self, when: datetime) -> None:
        self.last_login_at = when
        self.touch()

    def change_role(self, new_role: UserRole) -> None:
        self.role = new_role
        self.touch()

    def verify_email(self) -> None:
        self.is_email_verified = True
        self.touch()

    def has_role(self, *roles: UserRole) -> bool:
        return self.role in roles


@dataclass
class TeamMembership(SoftDeletableEntity):
    """Association between a user and a team."""

    team_id: UUID = field(default_factory=lambda: UUID(int=0))
    user_id: UUID = field(default_factory=lambda: UUID(int=0))
    is_lead: bool = False
```

### backend/app/domain/entities/project.py

```python
"""Project entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.value_objects import Slug


@dataclass
class Project(SoftDeletableEntity):
    """A project within a team that groups sprints and work items."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    team_id: UUID = field(default_factory=lambda: UUID(int=0))
    name: str = ""
    key: str = ""
    slug: Slug = field(default_factory=lambda: Slug("default"))
    description: str | None = None
    start_date: date | None = None
    target_end_date: date | None = None
    is_archived: bool = False

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Project name is required")
        if not self.key or len(self.key) < 2 or len(self.key) > 12:
            raise ValidationError("Project key must be between 2 and 12 characters")
        if not self.key.isalnum() or not self.key.isupper():
            raise ValidationError("Project key must be uppercase alphanumeric")
        if self.start_date and self.target_end_date and self.target_end_date < self.start_date:
            raise ValidationError("Target end date cannot be before start date")

    def archive(self) -> None:
        self.is_archived = True
        self.touch()

    def unarchive(self) -> None:
        self.is_archived = False
        self.touch()

    def rename(self, new_name: str) -> None:
        if not new_name.strip():
            raise ValidationError("Project name is required")
        self.name = new_name.strip()
        self.touch()
```

### backend/app/domain/entities/sprint.py

```python
"""Sprint entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import SprintStatus
from app.domain.value_objects import DateRange


@dataclass
class Sprint(SoftDeletableEntity):
    """A time-boxed sprint containing work items."""

    project_id: UUID = field(default_factory=lambda: UUID(int=0))
    name: str = ""
    goal: str | None = None
    start_date: date = field(default_factory=date.today)
    end_date: date = field(default_factory=date.today)
    status: SprintStatus = SprintStatus.PLANNED
    started_at: datetime | None = None
    completed_at: datetime | None = None
    planned_capacity: int = 0
    completed_points: int = 0

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Sprint name is required")
        if self.end_date < self.start_date:
            raise ValidationError("Sprint end date cannot be before start date")
        if self.planned_capacity < 0:
            raise ValidationError("Planned capacity cannot be negative")

    @property
    def date_range(self) -> DateRange:
        return DateRange(self.start_date, self.end_date)

    @property
    def is_active(self) -> bool:
        return self.status == SprintStatus.ACTIVE

    def start(self) -> None:
        if self.status != SprintStatus.PLANNED:
            raise BusinessRuleViolationError(
                f"Cannot start sprint from status {self.status.value}"
            )
        self.status = SprintStatus.ACTIVE
        self.started_at = datetime.now(timezone.utc)
        self.touch()

    def complete(self, completed_points: int) -> None:
        if self.status != SprintStatus.ACTIVE:
            raise BusinessRuleViolationError(
                f"Cannot complete sprint from status {self.status.value}"
            )
        if completed_points < 0:
            raise ValidationError("Completed points cannot be negative")
        self.status = SprintStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.completed_points = completed_points
        self.touch()

    def cancel(self) -> None:
        if self.status == SprintStatus.COMPLETED:
            raise BusinessRuleViolationError("Cannot cancel a completed sprint")
        self.status = SprintStatus.CANCELLED
        self.touch()

    @property
    def completion_rate(self) -> float:
        if self.planned_capacity == 0:
            return 0.0
        return round(self.completed_points / self.planned_capacity, 4)
```

================================================================================

### backend/app/domain/entities/work_item.py

```python
"""Work item entity - stories, tasks, bugs, epics, spikes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType


@dataclass
class WorkItem(SoftDeletableEntity):
    """A unit of engineering work traceable to business outcomes."""

    project_id: UUID = field(default_factory=lambda: UUID(int=0))
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    external_key: str | None = None
    title: str = ""
    description: str | None = None
    item_type: WorkItemType = WorkItemType.STORY
    status: WorkItemStatus = WorkItemStatus.BACKLOG
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    story_points: int | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    labels: list[str] = field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Work item title is required")
        if len(self.title) > 500:
            raise ValidationError("Work item title must be 500 characters or fewer")
        if self.story_points is not None and self.story_points < 0:
            raise ValidationError("Story points cannot be negative")
        if self.estimated_hours is not None and self.estimated_hours < 0:
            raise ValidationError("Estimated hours cannot be negative")
        if self.actual_hours is not None and self.actual_hours < 0:
            raise ValidationError("Actual hours cannot be negative")
        if self.item_type == WorkItemType.EPIC and self.epic_id is not None:
            raise ValidationError("An epic cannot belong to another epic")
        if self.parent_id is not None and self.parent_id == self.id:
            raise ValidationError("Work item cannot be its own parent")

    @property
    def is_completed(self) -> bool:
        return self.status == WorkItemStatus.DONE

    @property
    def is_in_flight(self) -> bool:
        return self.status in {WorkItemStatus.IN_PROGRESS, WorkItemStatus.IN_REVIEW}

    def assign_to_sprint(self, sprint_id: UUID) -> None:
        if self.is_completed:
            raise BusinessRuleViolationError("Cannot reassign a completed work item")
        self.sprint_id = sprint_id
        self.touch()

    def remove_from_sprint(self) -> None:
        if self.is_completed:
            raise BusinessRuleViolationError("Cannot remove a completed work item from sprint")
        self.sprint_id = None
        self.touch()

    def start(self) -> None:
        if self.status not in {WorkItemStatus.BACKLOG, WorkItemStatus.TODO}:
            raise BusinessRuleViolationError(
                f"Cannot start work item from status {self.status.value}"
            )
        self.status = WorkItemStatus.IN_PROGRESS
        self.started_at = datetime.now(timezone.utc)
        self.touch()

    def send_for_review(self) -> None:
        if self.status != WorkItemStatus.IN_PROGRESS:
            raise BusinessRuleViolationError(
                "Work item must be in progress to be sent for review"
            )
        self.status = WorkItemStatus.IN_REVIEW
        self.touch()

    def complete(self, actual_hours: float | None = None) -> None:
        if self.status in {WorkItemStatus.DONE, WorkItemStatus.CANCELLED}:
            raise BusinessRuleViolationError(
                f"Cannot complete work item from status {self.status.value}"
            )
        if actual_hours is not None:
            if actual_hours < 0:
                raise ValidationError("Actual hours cannot be negative")
            self.actual_hours = actual_hours
        self.status = WorkItemStatus.DONE
        self.completed_at = datetime.now(timezone.utc)
        self.touch()

    def cancel(self) -> None:
        if self.status == WorkItemStatus.DONE:
            raise BusinessRuleViolationError("Cannot cancel a completed work item")
        self.status = WorkItemStatus.CANCELLED
        self.touch()

    def reassign(self, user_id: UUID | None) -> None:
        self.assignee_id = user_id
        self.touch()

    def add_label(self, label: str) -> None:
        normalized = label.strip().lower()
        if not normalized:
            raise ValidationError("Label cannot be empty")
        if normalized not in self.labels:
            self.labels.append(normalized)
            self.touch()

    def remove_label(self, label: str) -> None:
        normalized = label.strip().lower()
        if normalized in self.labels:
            self.labels.remove(normalized)
            self.touch()
```

### backend/app/domain/entities/business_outcome.py

```python
"""Business outcome entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import OutcomeStatus


@dataclass
class BusinessOutcome(SoftDeletableEntity):
    """A measurable business outcome that engineering work should influence."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    owner_id: UUID | None = None
    name: str = ""
    description: str | None = None
    hypothesis: str | None = None
    status: OutcomeStatus = OutcomeStatus.PROPOSED
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = None
    financial_impact_estimate: Decimal | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("Outcome name is required")
        if len(self.name) > 300:
            raise ValidationError("Outcome name must be 300 characters or fewer")
        if self.confidence_score is not None:
            if self.confidence_score < Decimal("0") or self.confidence_score > Decimal("100"):
                raise ValidationError("Confidence score must be between 0 and 100")

    @property
    def progress_percent(self) -> Decimal:
        """Return progress percentage from baseline toward target."""
        if self.baseline_value is None or self.target_value is None or self.current_value is None:
            return Decimal("0")
        span = self.target_value - self.baseline_value
        if span == 0:
            return Decimal("100") if self.current_value >= self.target_value else Decimal("0")
        achieved = self.current_value - self.baseline_value
        pct = (achieved / span) * Decimal("100")
        if pct < 0:
            return Decimal("0")
        if pct > 100:
            return Decimal("100")
        return pct.quantize(Decimal("0.01"))

    def activate(self) -> None:
        if self.status != OutcomeStatus.PROPOSED:
            raise BusinessRuleViolationError(
                f"Cannot activate outcome from status {self.status.value}"
            )
        self.status = OutcomeStatus.ACTIVE
        self.touch()

    def mark_at_risk(self) -> None:
        self.status = OutcomeStatus.AT_RISK
        self.touch()

    def mark_off_track(self) -> None:
        self.status = OutcomeStatus.OFF_TRACK
        self.touch()

    def achieve(self) -> None:
        self.status = OutcomeStatus.ACHIEVED
        self.touch()

    def abandon(self) -> None:
        self.status = OutcomeStatus.ABANDONED
        self.touch()

    def update_current_value(self, value: Decimal) -> None:
        self.current_value = value
        self.touch()
```

### backend/app/domain/entities/kpi.py

```python
"""KPI entity and metric snapshots."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import KPIDirection, KPIUnit


@dataclass
class KPI(SoftDeletableEntity):
    """A Key Performance Indicator tracked by the organization."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str = ""
    description: str | None = None
    unit: KPIUnit = KPIUnit.COUNT
    currency: str | None = None
    direction: KPIDirection = KPIDirection.INCREASE
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = None
    refresh_frequency_hours: int | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("KPI name is required")
        if self.unit == KPIUnit.CURRENCY and not self.currency:
            raise ValidationError("Currency is required for currency-typed KPIs")
        if self.currency:
            code = self.currency.strip().upper()
            if len(code) != 3 or not code.isalpha():
                raise ValidationError(f"Invalid currency code: {self.currency}")
            self.currency = code
        if self.refresh_frequency_hours is not None and self.refresh_frequency_hours <= 0:
            raise ValidationError("Refresh frequency must be positive")

    def record_current_value(self, value: Decimal) -> None:
        self.current_value = value
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()

    def activate(self) -> None:
        self.is_active = True
        self.touch()

    @property
    def delta_from_baseline(self) -> Decimal | None:
        if self.baseline_value is None or self.current_value is None:
            return None
        return self.current_value - self.baseline_value

    @property
    def is_on_track(self) -> bool:
        """Return True when KPI trend matches desired direction."""
        if self.baseline_value is None or self.current_value is None:
            return False
        if self.direction == KPIDirection.INCREASE:
            return self.current_value >= self.baseline_value
        if self.direction == KPIDirection.DECREASE:
            return self.current_value <= self.baseline_value
        # MAINTAIN: within +/- 5% band of baseline
        if self.baseline_value == 0:
            return self.current_value == 0
        tolerance = abs(self.baseline_value) * Decimal("0.05")
        return abs(self.current_value - self.baseline_value) <= tolerance


@dataclass
class MetricSnapshot(SoftDeletableEntity):
    """A point-in-time snapshot of a KPI's value."""

    kpi_id: UUID = field(default_factory=lambda: UUID(int=0))
    value: Decimal = Decimal("0")
    recorded_at: datetime = field(default_factory=datetime.utcnow)
    source: str | None = None
    notes: str | None = None
    context: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            self.value = Decimal(str(self.value))
```

### backend/app/domain/entities/okr.py

```python
"""OKR (Objectives and Key Results) entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import OKRStatus, OKRType


@dataclass
class Objective(SoftDeletableEntity):
    """A qualitative goal to be achieved in a period."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    team_id: UUID | None = None
    owner_id: UUID | None = None
    parent_id: UUID | None = None
    title: str = ""
    description: str | None = None
    okr_type: OKRType = OKRType.TEAM
    status: OKRStatus = OKRStatus.DRAFT
    period_start: date = field(default_factory=date.today)
    period_end: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Objective title is required")
        if self.period_end < self.period_start:
            raise ValidationError("Period end cannot be before period start")
        if self.okr_type == OKRType.TEAM and self.team_id is None:
            raise ValidationError("Team objectives require a team_id")

    def activate(self) -> None:
        if self.status != OKRStatus.DRAFT:
            raise BusinessRuleViolationError(
                f"Cannot activate objective from status {self.status.value}"
            )
        self.status = OKRStatus.ACTIVE
        self.touch()

    def achieve(self) -> None:
        self.status = OKRStatus.ACHIEVED
        self.touch()

    def miss(self) -> None:
        self.status = OKRStatus.MISSED
        self.touch()

    def cancel(self) -> None:
        self.status = OKRStatus.CANCELLED
        self.touch()


@dataclass
class KeyResult(SoftDeletableEntity):
    """A measurable outcome that indicates progress on an objective."""

    objective_id: UUID = field(default_factory=lambda: UUID(int=0))
    kpi_id: UUID | None = None
    title: str = ""
    description: str | None = None
    baseline_value: Decimal = Decimal("0")
    target_value: Decimal = Decimal("0")
    current_value: Decimal = Decimal("0")
    weight: Decimal = Decimal("1")
    status: OKRStatus = OKRStatus.ACTIVE

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Key result title is required")
        for field_name in ("baseline_value", "target_value", "current_value", "weight"):
            val = getattr(self, field_name)
            if not isinstance(val, Decimal):
                setattr(self, field_name, Decimal(str(val)))
        if self.weight <= 0:
            raise ValidationError("Weight must be positive")

    @property
    def progress_percent(self) -> Decimal:
        span = self.target_value - self.baseline_value
        if span == 0:
            return (
                Decimal("100")
                if self.current_value >= self.target_value
                else Decimal("0")
            )
        achieved = self.current_value - self.baseline_value
        pct = (achieved / span) * Decimal("100")
        if pct < 0:
            return Decimal("0")
        if pct > 100:
            return Decimal("100")
        return pct.quantize(Decimal("0.01"))

    def update_current_value(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        self.current_value = value
        self.touch()
```

### backend/app/domain/entities/attribution.py

```python
"""Outcome attribution entity - links work items to business outcomes."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import SoftDeletableEntity
from app.domain.enums import AttributionMethod, AttributionStrength


@dataclass
class OutcomeAttribution(SoftDeletableEntity):
    """Links a work item (or sprint) to a business outcome or KPI."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    work_item_id: UUID | None = None
    sprint_id: UUID | None = None
    outcome_id: UUID | None = None
    kpi_id: UUID | None = None
    key_result_id: UUID | None = None
    attributed_by_id: UUID | None = None
    method: AttributionMethod = AttributionMethod.MANUAL
    strength: AttributionStrength = AttributionStrength.CONTRIBUTING
    weight: Decimal = Decimal("1.0")
    confidence: Decimal = Decimal("50")
    estimated_value: Decimal | None = None
    rationale: str | None = None

    def __post_init__(self) -> None:
        if self.work_item_id is None and self.sprint_id is None:
            raise ValidationError(
                "Attribution must reference at least one of work_item_id or sprint_id"
            )
        if self.outcome_id is None and self.kpi_id is None and self.key_result_id is None:
            raise ValidationError(
                "Attribution must reference an outcome, KPI, or key result"
            )
        for field_name in ("weight", "confidence"):
            val = getattr(self, field_name)
            if not isinstance(val, Decimal):
                setattr(self, field_name, Decimal(str(val)))
        if self.weight <= 0:
            raise ValidationError("Weight must be positive")
        if self.confidence < Decimal("0") or self.confidence > Decimal("100"):
            raise ValidationError("Confidence must be between 0 and 100")

    def update_strength(self, strength: AttributionStrength) -> None:
        self.strength = strength
        self.touch()

    def update_confidence(self, confidence: Decimal) -> None:
        if not isinstance(confidence, Decimal):
            confidence = Decimal(str(confidence))
        if confidence < Decimal("0") or confidence > Decimal("100"):
            raise ValidationError("Confidence must be between 0 and 100")
        self.confidence = confidence
        self.touch()


@dataclass
class Evidence(SoftDeletableEntity):
    """Supporting evidence for an attribution."""

    attribution_id: UUID = field(default_factory=lambda: UUID(int=0))
    author_id: UUID | None = None
    title: str = ""
    content: str = ""
    source_url: str | None = None
    evidence_type: str = "note"

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Evidence title is required")
        if not self.content or not self.content.strip():
            raise ValidationError("Evidence content is required")
```

### backend/app/domain/entities/notification.py

```python
"""Notification entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import Entity
from app.domain.enums import NotificationChannel, NotificationStatus


@dataclass
class Notification(Entity):
    """A notification delivered to a user."""

    recipient_id: UUID = field(default_factory=lambda: UUID(int=0))
    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    title: str = ""
    body: str = ""
    channel: NotificationChannel = NotificationChannel.IN_APP
    status: NotificationStatus = NotificationStatus.PENDING
    event_type: str = "generic"
    subject_type: str | None = None
    subject_id: UUID | None = None
    action_url: str | None = None
    sent_at: datetime | None = None
    read_at: datetime | None = None
    error_message: str | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("Notification title is required")
        if not self.body or not self.body.strip():
            raise ValidationError("Notification body is required")

    def mark_sent(self) -> None:
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.now(timezone.utc)
        self.touch()

    def mark_read(self) -> None:
        if self.status not in {NotificationStatus.SENT, NotificationStatus.PENDING}:
            return
        self.status = NotificationStatus.READ
        self.read_at = datetime.now(timezone.utc)
        self.touch()

    def mark_failed(self, error: str) -> None:
        self.status = NotificationStatus.FAILED
        self.error_message = error
        self.touch()
```

### backend/app/domain/entities/audit_log.py

```python
"""Audit log entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import Entity
from app.domain.enums import AuditAction


@dataclass
class AuditLog(Entity):
    """An immutable audit event."""

    organization_id: UUID = field(default_factory=lambda: UUID(int=0))
    actor_id: UUID | None = None
    action: AuditAction = AuditAction.CREATE
    resource_type: str = ""
    resource_id: UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    changes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.resource_type or not self.resource_type.strip():
            raise ValidationError("resource_type is required")
```

### backend/app/domain/repositories/base.py

```python
"""Repository protocols - abstract data-access contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from app.domain.entities.base import Entity

TEntity = TypeVar("TEntity", bound=Entity)


class Repository(ABC, Generic[TEntity]):
    """Abstract base repository for entities."""

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> TEntity | None:
        """Retrieve entity by its ID or return None."""

    @abstractmethod
    def add(self, entity: TEntity) -> TEntity:
        """Persist a new entity."""

    @abstractmethod
    def update(self, entity: TEntity) -> TEntity:
        """Persist changes to an existing entity."""

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """Delete (soft or hard) an entity by ID."""

    @abstractmethod
    def exists(self, entity_id: UUID) -> bool:
        """Return True if an entity with the given ID exists."""


class UnitOfWork(ABC):
    """Abstract unit-of-work for transactional consistency."""

    @abstractmethod
    def __enter__(self) -> UnitOfWork: ...

    @abstractmethod
    def __exit__(self, exc_type: object, exc: object, tb: object) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
```

### backend/app/domain/repositories/interfaces.py

```python
"""Concrete repository interfaces for each aggregate."""

from __future__ import annotations

from abc import abstractmethod
from datetime import date
from typing import Sequence
from uuid import UUID

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
from app.domain.repositories.base import Repository


class OrganizationRepository(Repository[Organization]):
    @abstractmethod
    def get_by_slug(self, slug: str) -> Organization | None: ...

    @abstractmethod
    def list_all(self, limit: int, offset: int) -> Sequence[Organization]: ...


class TeamRepository(Repository[Team]):
    @abstractmethod
    def list_by_organization(self, organization_id: UUID) -> Sequence[Team]: ...

    @abstractmethod
    def get_by_slug(self, organization_id: UUID, slug: str) -> Team | None: ...


class UserRepository(Repository[User]):
    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[User]: ...


class TeamMembershipRepository(Repository[TeamMembership]):
    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[TeamMembership]: ...

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> Sequence[TeamMembership]: ...

    @abstractmethod
    def get_by_team_and_user(
        self, team_id: UUID, user_id: UUID
    ) -> TeamMembership | None: ...


class ProjectRepository(Repository[Project]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[Project]: ...

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[Project]: ...

    @abstractmethod
    def get_by_key(self, organization_id: UUID, key: str) -> Project | None: ...


class SprintRepository(Repository[Sprint]):
    @abstractmethod
    def list_by_project(
        self, project_id: UUID, limit: int, offset: int
    ) -> Sequence[Sprint]: ...

    @abstractmethod
    def get_active_for_project(self, project_id: UUID) -> Sprint | None: ...

    @abstractmethod
    def list_completed_in_range(
        self, organization_id: UUID, start: date, end: date
    ) -> Sequence[Sprint]: ...


class WorkItemRepository(Repository[WorkItem]):
    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[WorkItem]: ...

    @abstractmethod
    def list_by_project(
        self, project_id: UUID, limit: int, offset: int
    ) -> Sequence[WorkItem]: ...

    @abstractmethod
    def list_by_assignee(self, user_id: UUID) -> Sequence[WorkItem]: ...

    @abstractmethod
    def list_unattributed(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[WorkItem]: ...


class BusinessOutcomeRepository(Repository[BusinessOutcome]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[BusinessOutcome]: ...

    @abstractmethod
    def list_off_track(self, organization_id: UUID) -> Sequence[BusinessOutcome]: ...


class KPIRepository(Repository[KPI]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[KPI]: ...

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[KPI]: ...


class MetricSnapshotRepository(Repository[MetricSnapshot]):
    @abstractmethod
    def list_by_kpi(
        self, kpi_id: UUID, limit: int, offset: int
    ) -> Sequence[MetricSnapshot]: ...

    @abstractmethod
    def latest_for_kpi(self, kpi_id: UUID) -> MetricSnapshot | None: ...


class ObjectiveRepository(Repository[Objective]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[Objective]: ...

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[Objective]: ...


class KeyResultRepository(Repository[KeyResult]):
    @abstractmethod
    def list_by_objective(self, objective_id: UUID) -> Sequence[KeyResult]: ...


class AttributionRepository(Repository[OutcomeAttribution]):
    @abstractmethod
    def list_by_work_item(self, work_item_id: UUID) -> Sequence[OutcomeAttribution]: ...

    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[OutcomeAttribution]: ...

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[OutcomeAttribution]: ...

    @abstractmethod
    def list_by_kpi(self, kpi_id: UUID) -> Sequence[OutcomeAttribution]: ...


class EvidenceRepository(Repository[Evidence]):
    @abstractmethod
    def list_by_attribution(self, attribution_id: UUID) -> Sequence[Evidence]: ...


class NotificationRepository(Repository[Notification]):
    @abstractmethod
    def list_by_recipient(
        self, recipient_id: UUID, limit: int, offset: int
    ) -> Sequence[Notification]: ...

    @abstractmethod
    def count_unread(self, recipient_id: UUID) -> int: ...


class AuditLogRepository(Repository[AuditLog]):
    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, limit: int, offset: int
    ) -> Sequence[AuditLog]: ...

    @abstractmethod
    def list_by_resource(
        self, resource_type: str, resource_id: UUID
    ) -> Sequence[AuditLog]: ...
```

### backend/app/domain/services/attribution_service.py

```python
"""Domain service for computing outcome attribution and impact."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence

from app.domain.entities.attribution import OutcomeAttribution
from app.domain.entities.sprint import Sprint
from app.domain.entities.work_item import WorkItem
from app.domain.enums import AttributionStrength, SprintStatus, WorkItemStatus


_STRENGTH_WEIGHTS: dict[AttributionStrength, Decimal] = {
    AttributionStrength.PRIMARY: Decimal("1.0"),
    AttributionStrength.CONTRIBUTING: Decimal("0.6"),
    AttributionStrength.SUPPORTING: Decimal("0.3"),
    AttributionStrength.NONE: Decimal("0.0"),
}


@dataclass(frozen=True)
class ImpactScore:
    """Computed impact for a set of attributions."""

    total_score: Decimal
    weighted_confidence: Decimal
    estimated_value: Decimal
    attribution_count: int


class AttributionDomainService:
    """Pure domain logic for reasoning about attribution."""

    @staticmethod
    def strength_factor(strength: AttributionStrength) -> Decimal:
        return _STRENGTH_WEIGHTS[strength]

    @classmethod
    def compute_impact(cls, attributions: Sequence[OutcomeAttribution]) -> ImpactScore:
        """Compute an aggregate impact score across attributions."""
        if not attributions:
            return ImpactScore(
                total_score=Decimal("0"),
                weighted_confidence=Decimal("0"),
                estimated_value=Decimal("0"),
                attribution_count=0,
            )

        total_score = Decimal("0")
        total_weight = Decimal("0")
        weighted_confidence = Decimal("0")
        estimated_value = Decimal("0")

        for attr in attributions:
            factor = cls.strength_factor(attr.strength)
            score = attr.weight * factor * (attr.confidence / Decimal("100"))
            total_score += score
            total_weight += attr.weight
            weighted_confidence += attr.confidence * attr.weight
            if attr.estimated_value is not None:
                estimated_value += attr.estimated_value

        avg_confidence = (
            weighted_confidence / total_weight if total_weight > 0 else Decimal("0")
        )

        return ImpactScore(
            total_score=total_score.quantize(Decimal("0.0001")),
            weighted_confidence=avg_confidence.quantize(Decimal("0.01")),
            estimated_value=estimated_value.quantize(Decimal("0.01")),
            attribution_count=len(attributions),
        )

    @staticmethod
    def find_unattributed_completed_items(
        work_items: Sequence[WorkItem],
        attributions_by_work_item: dict,
    ) -> list[WorkItem]:
        """Return completed work items that have no attributions."""
        return [
            item
            for item in work_items
            if item.status == WorkItemStatus.DONE
            and not attributions_by_work_item.get(item.id)
        ]

    @staticmethod
    def sprint_roi(
        sprint: Sprint,
        attributions: Sequence[OutcomeAttribution],
        estimated_cost: Decimal,
    ) -> Decimal:
        """Compute ROI as (estimated_value - cost) / cost for a completed sprint."""
        if sprint.status != SprintStatus.COMPLETED:
            return Decimal("0")
        if estimated_cost <= 0:
            return Decimal("0")
        total_value = sum(
            (a.estimated_value for a in attributions if a.estimated_value is not None),
            start=Decimal("0"),
        )
        roi = (total_value - estimated_cost) / estimated_cost
        return roi.quantize(Decimal("0.0001"))
```

================================================================================

### backend/app/domain/services/__init__.py

```python
"""Domain services - stateless business logic."""

from app.domain.services.attribution_service import AttributionDomainService, ImpactScore

__all__ = ["AttributionDomainService", "ImpactScore"]
```

### backend/app/domain/services/sprint_metrics_service.py

```python
"""Domain service for computing sprint performance metrics."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence

from app.domain.entities.sprint import Sprint
from app.domain.entities.work_item import WorkItem
from app.domain.enums import SprintStatus, WorkItemStatus, WorkItemType


@dataclass(frozen=True)
class SprintMetrics:
    """Aggregated metrics for a sprint."""

    sprint_id: str
    total_items: int
    completed_items: int
    cancelled_items: int
    total_points_planned: int
    total_points_completed: int
    completion_rate: Decimal
    velocity: int
    bug_count: int
    story_count: int
    task_count: int
    scope_change_percent: Decimal


class SprintMetricsDomainService:
    """Compute sprint-level engineering metrics."""

    @staticmethod
    def compute(sprint: Sprint, work_items: Sequence[WorkItem]) -> SprintMetrics:
        """Compute metrics for a sprint given its work items."""
        total_items = len(work_items)
        completed_items = sum(1 for w in work_items if w.status == WorkItemStatus.DONE)
        cancelled_items = sum(
            1 for w in work_items if w.status == WorkItemStatus.CANCELLED
        )
        total_points_planned = sum(w.story_points or 0 for w in work_items)
        total_points_completed = sum(
            (w.story_points or 0) for w in work_items if w.status == WorkItemStatus.DONE
        )
        bug_count = sum(1 for w in work_items if w.item_type == WorkItemType.BUG)
        story_count = sum(1 for w in work_items if w.item_type == WorkItemType.STORY)
        task_count = sum(1 for w in work_items if w.item_type == WorkItemType.TASK)

        completion_rate = (
            (Decimal(total_points_completed) / Decimal(total_points_planned)).quantize(
                Decimal("0.0001")
            )
            if total_points_planned > 0
            else Decimal("0")
        )

        scope_change_percent = (
            (
                Decimal(total_points_planned - sprint.planned_capacity)
                / Decimal(sprint.planned_capacity)
                * Decimal("100")
            ).quantize(Decimal("0.01"))
            if sprint.planned_capacity > 0
            else Decimal("0")
        )

        velocity = total_points_completed if sprint.status == SprintStatus.COMPLETED else 0

        return SprintMetrics(
            sprint_id=str(sprint.id),
            total_items=total_items,
            completed_items=completed_items,
            cancelled_items=cancelled_items,
            total_points_planned=total_points_planned,
            total_points_completed=total_points_completed,
            completion_rate=completion_rate,
            velocity=velocity,
            bug_count=bug_count,
            story_count=story_count,
            task_count=task_count,
            scope_change_percent=scope_change_percent,
        )

    @staticmethod
    def rolling_velocity(sprints: Sequence[Sprint], window: int = 3) -> Decimal:
        """Return average velocity across the last N completed sprints."""
        completed = [s for s in sprints if s.status == SprintStatus.COMPLETED]
        if not completed:
            return Decimal("0")
        completed.sort(key=lambda s: s.completed_at or s.end_date, reverse=True)
        subset = completed[:window]
        total = sum(s.completed_points for s in subset)
        return (Decimal(total) / Decimal(len(subset))).quantize(Decimal("0.01"))
```

### backend/app/domain/services/outcome_health_service.py

```python
"""Domain service for evaluating business outcome health."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.enums import OutcomeStatus


@dataclass(frozen=True)
class OutcomeHealth:
    """Health signal for a business outcome."""

    outcome_id: str
    progress_percent: Decimal
    time_elapsed_percent: Decimal
    health_score: Decimal
    is_at_risk: bool
    is_off_track: bool
    recommended_status: OutcomeStatus


class OutcomeHealthDomainService:
    """Assess whether an outcome is on track, at risk, or off track."""

    AT_RISK_GAP = Decimal("15")
    OFF_TRACK_GAP = Decimal("30")

    @classmethod
    def evaluate(
        cls,
        outcome: BusinessOutcome,
        as_of: date | None = None,
        period_start: date | None = None,
    ) -> OutcomeHealth:
        """Return a health assessment relative to progress vs. time elapsed."""
        today = as_of or date.today()
        progress = outcome.progress_percent

        time_elapsed = Decimal("0")
        if outcome.target_date and period_start:
            total_days = (outcome.target_date - period_start).days
            elapsed_days = (today - period_start).days
            if total_days > 0:
                pct = (Decimal(elapsed_days) / Decimal(total_days)) * Decimal("100")
                time_elapsed = max(Decimal("0"), min(Decimal("100"), pct))
        elif outcome.target_date:
            days_left = (outcome.target_date - today).days
            time_elapsed = (
                Decimal("100") if days_left <= 0 else Decimal("50")
            )

        gap = time_elapsed - progress
        is_off_track = gap >= cls.OFF_TRACK_GAP
        is_at_risk = gap >= cls.AT_RISK_GAP and not is_off_track

        health_score = (Decimal("100") - max(Decimal("0"), gap)).quantize(Decimal("0.01"))

        if outcome.status == OutcomeStatus.ACHIEVED:
            recommended = OutcomeStatus.ACHIEVED
        elif outcome.status == OutcomeStatus.ABANDONED:
            recommended = OutcomeStatus.ABANDONED
        elif is_off_track:
            recommended = OutcomeStatus.OFF_TRACK
        elif is_at_risk:
            recommended = OutcomeStatus.AT_RISK
        elif progress >= Decimal("100"):
            recommended = OutcomeStatus.ACHIEVED
        else:
            recommended = OutcomeStatus.ACTIVE

        return OutcomeHealth(
            outcome_id=str(outcome.id),
            progress_percent=progress,
            time_elapsed_percent=time_elapsed.quantize(Decimal("0.01")),
            health_score=health_score,
            is_at_risk=is_at_risk,
            is_off_track=is_off_track,
            recommended_status=recommended,
        )
```

### backend/app/domain/services/authorization_service.py

```python
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
```

### backend/app/infrastructure/__init__.py

```python
"""Infrastructure layer - persistence, external integrations, cross-cutting concerns."""
```

### backend/app/infrastructure/persistence/__init__.py

```python
"""Persistence infrastructure - SQLAlchemy models, mappers, repositories."""
```

### backend/app/infrastructure/persistence/database.py

```python
"""Database engine and session management."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

_engine: Engine = create_engine(
    settings.database_url,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=settings.DATABASE_ECHO,
    future=True,
)

SessionFactory = sessionmaker(
    bind=_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
)


def get_engine() -> Engine:
    """Return the SQLAlchemy engine."""
    return _engine


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Iterator[Session]:
    """FastAPI dependency for obtaining a database session."""
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
```

### backend/app/infrastructure/persistence/models/base.py

```python
"""SQLAlchemy declarative base and mixins."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UUIDPrimaryKeyMixin:
    """Provides a UUID primary key column."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )


class TimestampMixin:
    """Provides created_at and updated_at columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """Provides deleted_at column for soft deletion."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )
```

### backend/app/infrastructure/persistence/models/organization.py

```python
"""ORM models for Organization and Team."""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class OrganizationModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Organization table."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    billing_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    teams: Mapped[list["TeamModel"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )


class TeamModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Team table."""

    __tablename__ = "teams"
    __table_args__ = (
        UniqueConstraint("organization_id", "slug", name="uq_teams_org_slug"),
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    organization: Mapped[OrganizationModel] = relationship(back_populates="teams")
```

### backend/app/infrastructure/persistence/models/user.py

```python
"""ORM models for User and TeamMembership."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class UserModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """User table."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="viewer")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="invited")
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class TeamMembershipModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Team membership association table."""

    __tablename__ = "team_memberships"
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_memberships_team_user"),
    )

    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    is_lead: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
```

### backend/app/infrastructure/persistence/models/project.py

```python
"""ORM model for Project."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class ProjectModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Project table."""

    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("organization_id", "key", name="uq_projects_org_key"),
        UniqueConstraint("organization_id", "slug", name="uq_projects_org_slug"),
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    key: Mapped[str] = mapped_column(String(12), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    target_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
```

### backend/app/infrastructure/persistence/models/sprint.py

```python
"""ORM model for Sprint."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class SprintModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Sprint table."""

    __tablename__ = "sprints"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    goal: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="planned", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    planned_capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
```

================================================================================

### backend/app/domain/repositories/__init__.py

```python
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
```

### backend/app/domain/repositories/specifications.py

```python
"""Query specifications used by repositories."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID


@dataclass(frozen=True)
class PageRequest:
    """Pagination request."""

    limit: int = 20
    offset: int = 0
    order_by: str = "created_at"
    descending: bool = True

    def __post_init__(self) -> None:
        if self.limit <= 0 or self.limit > 500:
            raise ValueError("limit must be between 1 and 500")
        if self.offset < 0:
            raise ValueError("offset cannot be negative")


@dataclass(frozen=True)
class WorkItemFilter:
    """Filter criteria for querying work items."""

    organization_id: UUID | None = None
    project_id: UUID | None = None
    sprint_id: UUID | None = None
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    epic_id: UUID | None = None
    item_types: tuple[str, ...] = field(default_factory=tuple)
    statuses: tuple[str, ...] = field(default_factory=tuple)
    priorities: tuple[str, ...] = field(default_factory=tuple)
    labels: tuple[str, ...] = field(default_factory=tuple)
    search: str | None = None
    completed_after: datetime | None = None
    completed_before: datetime | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class SprintFilter:
    """Filter criteria for querying sprints."""

    organization_id: UUID | None = None
    project_id: UUID | None = None
    statuses: tuple[str, ...] = field(default_factory=tuple)
    starts_after: date | None = None
    ends_before: date | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class OutcomeFilter:
    """Filter criteria for querying business outcomes."""

    organization_id: UUID | None = None
    owner_id: UUID | None = None
    statuses: tuple[str, ...] = field(default_factory=tuple)
    target_before: date | None = None
    target_after: date | None = None
    search: str | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class KPIFilter:
    """Filter criteria for querying KPIs."""

    organization_id: UUID | None = None
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    units: tuple[str, ...] = field(default_factory=tuple)
    is_active: bool | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class AttributionFilter:
    """Filter criteria for querying attributions."""

    organization_id: UUID | None = None
    work_item_id: UUID | None = None
    sprint_id: UUID | None = None
    outcome_id: UUID | None = None
    kpi_id: UUID | None = None
    key_result_id: UUID | None = None
    strengths: tuple[str, ...] = field(default_factory=tuple)
    methods: tuple[str, ...] = field(default_factory=tuple)
    include_deleted: bool = False


@dataclass(frozen=True)
class AuditLogFilter:
    """Filter criteria for querying audit logs."""

    organization_id: UUID | None = None
    actor_id: UUID | None = None
    resource_type: str | None = None
    resource_id: UUID | None = None
    actions: tuple[str, ...] = field(default_factory=tuple)
    occurred_after: datetime | None = None
    occurred_before: datetime | None = None


@dataclass(frozen=True)
class MetricSnapshotFilter:
    """Filter criteria for querying metric snapshots."""

    kpi_id: UUID | None = None
    recorded_after: datetime | None = None
    recorded_before: datetime | None = None
    source: str | None = None


@dataclass(frozen=True)
class NotificationFilter:
    """Filter criteria for querying notifications."""

    recipient_id: UUID | None = None
    organization_id: UUID | None = None
    statuses: tuple[str, ...] = field(default_factory=tuple)
    channels: tuple[str, ...] = field(default_factory=tuple)
    event_types: tuple[str, ...] = field(default_factory=tuple)
```

### backend/app/domain/repositories/organization_repository.py

```python
"""Repository contracts for Organization and Team aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.organization import Organization, Team
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class OrganizationRepositoryContract(Repository[Organization], ABC):
    """Repository contract for the Organization aggregate."""

    @abstractmethod
    def get_by_slug(self, slug: str) -> Organization | None:
        """Return an organization by its unique slug."""

    @abstractmethod
    def get_by_billing_email(self, email: str) -> Organization | None:
        """Return an organization by its billing email."""

    @abstractmethod
    def list_all(self, page: PageRequest) -> Sequence[Organization]:
        """Return a paginated list of organizations."""

    @abstractmethod
    def list_active(self, page: PageRequest) -> Sequence[Organization]:
        """Return active organizations."""

    @abstractmethod
    def count(self) -> int:
        """Return total organization count."""

    @abstractmethod
    def slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        """Return True when the slug is already in use."""


class TeamRepositoryContract(Repository[Team], ABC):
    """Repository contract for the Team aggregate."""

    @abstractmethod
    def get_by_slug(self, organization_id: UUID, slug: str) -> Team | None:
        """Return a team by organization and slug."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Team]:
        """Return teams in an organization."""

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> Sequence[Team]:
        """Return teams that a user belongs to."""

    @abstractmethod
    def count_by_organization(self, organization_id: UUID) -> int:
        """Return the count of teams in an organization."""

    @abstractmethod
    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when the slug is already in use in this organization."""
```

### backend/app/domain/repositories/user_repository.py

```python
"""Repository contracts for User and TeamMembership aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.user import TeamMembership, User
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class UserRepositoryContract(Repository[User], ABC):
    """Repository contract for the User aggregate."""

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Return a user by email (case-insensitive)."""

    @abstractmethod
    def email_exists(self, email: str, exclude_id: UUID | None = None) -> bool:
        """Return True when the email is already in use."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[User]:
        """Return users belonging to an organization."""

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[User]:
        """Return users who are members of a team."""

    @abstractmethod
    def list_by_role(
        self, organization_id: UUID, role: str, page: PageRequest
    ) -> Sequence[User]:
        """Return users of a given role in an organization."""

    @abstractmethod
    def search(
        self, organization_id: UUID, query: str, page: PageRequest
    ) -> Sequence[User]:
        """Search users within an organization."""

    @abstractmethod
    def count_by_organization(self, organization_id: UUID) -> int:
        """Return total user count for an organization."""


class TeamMembershipRepositoryContract(Repository[TeamMembership], ABC):
    """Repository contract for TeamMembership associations."""

    @abstractmethod
    def get_by_team_and_user(
        self, team_id: UUID, user_id: UUID
    ) -> TeamMembership | None:
        """Return a membership by team and user."""

    @abstractmethod
    def list_by_team(self, team_id: UUID) -> Sequence[TeamMembership]:
        """Return all memberships in a team."""

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> Sequence[TeamMembership]:
        """Return all memberships for a user."""

    @abstractmethod
    def remove_by_team_and_user(self, team_id: UUID, user_id: UUID) -> None:
        """Remove a user's membership from a team."""
```

### backend/app/domain/repositories/project_repository.py

```python
"""Repository contract for the Project aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.project import Project
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class ProjectRepositoryContract(Repository[Project], ABC):
    """Repository contract for the Project aggregate."""

    @abstractmethod
    def get_by_key(self, organization_id: UUID, key: str) -> Project | None:
        """Return a project by its unique key within an organization."""

    @abstractmethod
    def get_by_slug(self, organization_id: UUID, slug: str) -> Project | None:
        """Return a project by its slug within an organization."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        """Return projects in an organization."""

    @abstractmethod
    def list_by_team(
        self, team_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        """Return projects for a specific team."""

    @abstractmethod
    def key_exists(
        self, organization_id: UUID, key: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when a project key is already in use."""

    @abstractmethod
    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when a project slug is already in use."""

    @abstractmethod
    def count_by_organization(
        self, organization_id: UUID, include_archived: bool = False
    ) -> int:
        """Return project count for an organization."""
```

### backend/app/domain/repositories/sprint_repository.py

```python
"""Repository contract for the Sprint aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Sequence
from uuid import UUID

from app.domain.entities.sprint import Sprint
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest, SprintFilter


class SprintRepositoryContract(Repository[Sprint], ABC):
    """Repository contract for the Sprint aggregate."""

    @abstractmethod
    def list_by_project(
        self, project_id: UUID, page: PageRequest
    ) -> Sequence[Sprint]:
        """Return sprints for a project."""

    @abstractmethod
    def get_active_for_project(self, project_id: UUID) -> Sprint | None:
        """Return the currently active sprint for a project, if any."""

    @abstractmethod
    def list_completed_in_range(
        self, organization_id: UUID, start: date, end: date
    ) -> Sequence[Sprint]:
        """Return sprints completed within a date range for an organization."""

    @abstractmethod
    def list_active_for_organization(
        self, organization_id: UUID
    ) -> Sequence[Sprint]:
        """Return all currently active sprints across an organization."""

    @abstractmethod
    def find(self, spec: SprintFilter, page: PageRequest) -> Sequence[Sprint]:
        """Return sprints matching a filter specification."""

    @abstractmethod
    def count(self, spec: SprintFilter) -> int:
        """Return the count of sprints matching a filter specification."""

    @abstractmethod
    def latest_by_project(self, project_id: UUID, limit: int = 5) -> Sequence[Sprint]:
        """Return the most recent sprints in a project."""
```

### backend/app/domain/repositories/work_item_repository.py

```python
"""Repository contract for the WorkItem aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.work_item import WorkItem
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest, WorkItemFilter


class WorkItemRepositoryContract(Repository[WorkItem], ABC):
    """Repository contract for the WorkItem aggregate."""

    @abstractmethod
    def get_by_external_key(
        self, project_id: UUID, external_key: str
    ) -> WorkItem | None:
        """Return a work item by external key within a project."""

    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[WorkItem]:
        """Return work items assigned to a sprint."""

    @abstractmethod
    def list_by_project(
        self, project_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        """Return work items in a project."""

    @abstractmethod
    def list_by_epic(self, epic_id: UUID) -> Sequence[WorkItem]:
        """Return child work items of an epic."""

    @abstractmethod
    def list_by_parent(self, parent_id: UUID) -> Sequence[WorkItem]:
        """Return child work items of a parent."""

    @abstractmethod
    def list_by_assignee(
        self, user_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        """Return work items assigned to a user."""

    @abstractmethod
    def list_unattributed(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        """Return completed work items lacking outcome attributions."""

    @abstractmethod
    def find(self, spec: WorkItemFilter, page: PageRequest) -> Sequence[WorkItem]:
        """Return work items matching a filter specification."""

    @abstractmethod
    def count(self, spec: WorkItemFilter) -> int:
        """Return count of work items matching a filter."""

    @abstractmethod
    def bulk_reassign_sprint(
        self, work_item_ids: Sequence[UUID], sprint_id: UUID | None
    ) -> int:
        """Reassign multiple work items to a sprint (or unassign). Returns count updated."""
```

### backend/app/domain/repositories/outcome_repository.py

```python
"""Repository contract for the BusinessOutcome aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import OutcomeFilter, PageRequest


class BusinessOutcomeRepositoryContract(Repository[BusinessOutcome], ABC):
    """Repository contract for the BusinessOutcome aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes for an organization."""

    @abstractmethod
    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes owned by a user."""

    @abstractmethod
    def list_off_track(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        """Return outcomes flagged as off track."""

    @abstractmethod
    def list_at_risk(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        """Return outcomes flagged as at risk."""

    @abstractmethod
    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes with active status."""

    @abstractmethod
    def find(
        self, spec: OutcomeFilter, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        """Return outcomes matching a filter specification."""

    @abstractmethod
    def count(self, spec: OutcomeFilter) -> int:
        """Return count of outcomes matching a filter."""

    @abstractmethod
    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when an outcome with the given name exists in the organization."""
```

### backend/app/domain/repositories/kpi_repository.py

```python
"""Repository contracts for KPI and MetricSnapshot aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence
from uuid import UUID

from app.domain.entities.kpi import KPI, MetricSnapshot
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import (
    KPIFilter,
    MetricSnapshotFilter,
    PageRequest,
)


class KPIRepositoryContract(Repository[KPI], ABC):
    """Repository contract for the KPI aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[KPI]:
        """Return KPIs for an organization."""

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[KPI]:
        """Return KPIs linked to a specific business outcome."""

    @abstractmethod
    def list_by_owner(self, owner_id: UUID, page: PageRequest) -> Sequence[KPI]:
        """Return KPIs owned by a user."""

    @abstractmethod
    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[KPI]:
        """Return active KPIs in an organization."""

    @abstractmethod
    def find(self, spec: KPIFilter, page: PageRequest) -> Sequence[KPI]:
        """Return KPIs matching a filter."""

    @abstractmethod
    def count(self, spec: KPIFilter) -> int:
        """Return count of KPIs matching a filter."""

    @abstractmethod
    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        """Return True when a KPI name already exists in the organization."""


class MetricSnapshotRepositoryContract(Repository[MetricSnapshot], ABC):
    """Repository contract for MetricSnapshot records."""

    @abstractmethod
    def list_by_kpi(
        self, kpi_id: UUID, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        """Return snapshots for a KPI ordered by recorded_at descending."""

    @abstractmethod
    def latest_for_kpi(self, kpi_id: UUID) -> MetricSnapshot | None:
        """Return the most recent snapshot for a KPI."""

    @abstractmethod
    def list_in_range(
        self, kpi_id: UUID, start: datetime, end: datetime
    ) -> Sequence[MetricSnapshot]:
        """Return snapshots for a KPI within an inclusive time range."""

    @abstractmethod
    def find(
        self, spec: MetricSnapshotFilter, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        """Return snapshots matching a filter."""

    @abstractmethod
    def delete_older_than(self, kpi_id: UUID, cutoff: datetime) -> int:
        """Purge snapshots older than a cutoff. Returns count purged."""
```

### backend/app/domain/repositories/okr_repository.py

```python
"""Repository contracts for Objective and KeyResult aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.okr import KeyResult, Objective
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class ObjectiveRepositoryContract(Repository[Objective], ABC):
    """Repository contract for the Objective aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return objectives for an organization."""

    @abstractmethod
    def list_by_team(
        self, team_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return objectives for a team."""

    @abstractmethod
    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return objectives owned by a user."""

    @abstractmethod
    def list_by_parent(self, parent_id: UUID) -> Sequence[Objective]:
        """Return objectives that cascade from a parent objective."""

    @abstractmethod
    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        """Return active objectives for an organization."""

    @abstractmethod
    def count_by_organization(self, organization_id: UUID) -> int:
        """Return the number of objectives in an organization."""


class KeyResultRepositoryContract(Repository[KeyResult], ABC):
    """Repository contract for the KeyResult aggregate."""

    @abstractmethod
    def list_by_objective(self, objective_id: UUID) -> Sequence[KeyResult]:
        """Return key results attached to an objective."""

    @abstractmethod
    def list_by_kpi(self, kpi_id: UUID) -> Sequence[KeyResult]:
        """Return key results linked to a KPI."""

    @abstractmethod
    def count_by_objective(self, objective_id: UUID) -> int:
        """Return the number of key results on an objective."""

    @abstractmethod
    def delete_by_objective(self, objective_id: UUID) -> int:
        """Soft-delete all key results for an objective. Returns count deleted."""
```

### backend/app/domain/repositories/attribution_repository.py

```python
"""Repository contracts for OutcomeAttribution and Evidence aggregates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.attribution import Evidence, OutcomeAttribution
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import AttributionFilter, PageRequest


class AttributionRepositoryContract(Repository[OutcomeAttribution], ABC):
    """Repository contract for the OutcomeAttribution aggregate."""

    @abstractmethod
    def list_by_work_item(
        self, work_item_id: UUID
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions for a work item."""

    @abstractmethod
    def list_by_sprint(self, sprint_id: UUID) -> Sequence[OutcomeAttribution]:
        """Return attributions attached to a sprint."""

    @abstractmethod
    def list_by_outcome(self, outcome_id: UUID) -> Sequence[OutcomeAttribution]:
        """Return attributions referencing a business outcome."""

    @abstractmethod
    def list_by_kpi(self, kpi_id: UUID) -> Sequence[OutcomeAttribution]:
        """Return attributions referencing a KPI."""

    @abstractmethod
    def list_by_key_result(
        self, key_result_id: UUID
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions referencing a key result."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions across an organization."""

    @abstractmethod
    def find(
        self, spec: AttributionFilter, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        """Return attributions matching a filter."""

    @abstractmethod
    def count(self, spec: AttributionFilter) -> int:
        """Return count of attributions matching a filter."""

    @abstractmethod
    def exists_for_pair(
        self,
        work_item_id: UUID | None,
        sprint_id: UUID | None,
        outcome_id: UUID | None,
        kpi_id: UUID | None,
        key_result_id: UUID | None,
    ) -> bool:
        """Return True when an attribution linking the given subject to target exists."""


class EvidenceRepositoryContract(Repository[Evidence], ABC):
    """Repository contract for Evidence records."""

    @abstractmethod
    def list_by_attribution(self, attribution_id: UUID) -> Sequence[Evidence]:
        """Return evidence records linked to an attribution."""

    @abstractmethod
    def count_by_attribution(self, attribution_id: UUID) -> int:
        """Return count of evidence records for an attribution."""

    @abstractmethod
    def delete_by_attribution(self, attribution_id: UUID) -> int:
        """Soft-delete all evidence for an attribution. Returns count deleted."""
```

### backend/app/domain/repositories/notification_repository.py

```python
"""Repository contract for the Notification aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.notification import Notification
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import NotificationFilter, PageRequest


class NotificationRepositoryContract(Repository[Notification], ABC):
    """Repository contract for the Notification aggregate."""

    @abstractmethod
    def list_by_recipient(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        """Return notifications for a recipient ordered newest-first."""

    @abstractmethod
    def list_unread(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        """Return unread notifications for a recipient."""

    @abstractmethod
    def count_unread(self, recipient_id: UUID) -> int:
        """Return count of unread notifications for a recipient."""

    @abstractmethod
    def find(
        self, spec: NotificationFilter, page: PageRequest
    ) -> Sequence[Notification]:
        """Return notifications matching a filter."""

    @abstractmethod
    def mark_all_read(self, recipient_id: UUID) -> int:
        """Mark all pending/sent notifications as read. Returns count updated."""

    @abstractmethod
    def list_pending_for_delivery(self, limit: int) -> Sequence[Notification]:
        """Return pending notifications ready for outbound delivery."""
```

### backend/app/domain/repositories/audit_log_repository.py

```python
"""Repository contract for the AuditLog aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import AuditLogFilter, PageRequest


class AuditLogRepositoryContract(Repository[AuditLog], ABC):
    """Repository contract for the AuditLog aggregate."""

    @abstractmethod
    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        """Return audit log entries for an organization."""

    @abstractmethod
    def list_by_resource(
        self, resource_type: str, resource_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        """Return audit entries scoped to a specific resource."""

    @abstractmethod
    def list_by_actor(
        self, actor_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        """Return audit entries produced by a user."""

    @abstractmethod
    def find(self, spec: AuditLogFilter, page: PageRequest) -> Sequence[AuditLog]:
        """Return audit log entries matching a filter."""

    @abstractmethod
    def count(self, spec: AuditLogFilter) -> int:
        """Return count of audit entries matching a filter."""
```

================================================================================

### backend/app/infrastructure/persistence/models/__init__.py

```python
"""SQLAlchemy ORM models."""

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)
from app.infrastructure.persistence.models.organization import (
    OrganizationModel,
    TeamModel,
)
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.models.sprint import SprintModel
from app.infrastructure.persistence.models.user import TeamMembershipModel, UserModel

__all__ = [
    "Base",
    "SoftDeleteMixin",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    "OrganizationModel",
    "TeamModel",
    "ProjectModel",
    "SprintModel",
    "TeamMembershipModel",
    "UserModel",
]
```

### backend/app/infrastructure/persistence/models/work_item.py

```python
"""ORM model for WorkItem."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class WorkItemModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Work item table."""

    __tablename__ = "work_items"
    __table_args__ = (
        UniqueConstraint(
            "project_id", "external_key", name="uq_work_items_project_external_key"
        ),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sprint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sprints.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("work_items.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    epic_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("work_items.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    external_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(String(10000), nullable=True)
    item_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(32), nullable=False, default="medium")
    story_points: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    reporter_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    labels: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list, server_default="{}"
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

### backend/app/infrastructure/persistence/models/business_outcome.py

```python
"""ORM model for BusinessOutcome."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class BusinessOutcomeModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Business outcome table."""

    __tablename__ = "business_outcomes"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(String(4000), nullable=True)
    hypothesis: Mapped[str | None] = mapped_column(String(4000), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    baseline_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    target_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    current_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    financial_impact_estimate: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2), nullable=True
    )
```

### backend/app/infrastructure/persistence/models/kpi.py

```python
"""ORM models for KPI and MetricSnapshot."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class KPIModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """KPI table."""

    __tablename__ = "kpis"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    outcome_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business_outcomes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)
    baseline_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    target_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    current_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    data_source: Mapped[str | None] = mapped_column(String(500), nullable=True)
    refresh_frequency_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class MetricSnapshotModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Metric snapshot table."""

    __tablename__ = "metric_snapshots"

    kpi_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("kpis.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    value: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    source: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    context: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
```

### backend/app/infrastructure/persistence/models/okr.py

```python
"""ORM models for Objective and KeyResult."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class ObjectiveModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Objective table."""

    __tablename__ = "objectives"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    team_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("objectives.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(String(4000), nullable=True)
    okr_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)


class KeyResultModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Key result table."""

    __tablename__ = "key_results"

    objective_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("objectives.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kpi_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("kpis.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(String(4000), nullable=True)
    baseline_value: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    target_value: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    current_value: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(6, 3), nullable=False, default=Decimal("1"))
    status: Mapped[str] = mapped_column(String(32), nullable=False)
```

### backend/app/infrastructure/persistence/models/attribution.py

```python
"""ORM models for OutcomeAttribution and Evidence."""

from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class OutcomeAttributionModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Outcome attribution table."""

    __tablename__ = "outcome_attributions"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    work_item_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("work_items.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    sprint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sprints.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    outcome_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business_outcomes.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    kpi_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("kpis.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    key_result_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("key_results.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    attributed_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    method: Mapped[str] = mapped_column(String(32), nullable=False)
    strength: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    weight: Mapped[Decimal] = mapped_column(Numeric(6, 3), nullable=False, default=Decimal("1"))
    confidence: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=Decimal("50")
    )
    estimated_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 2), nullable=True)
    rationale: Mapped[str | None] = mapped_column(String(4000), nullable=True)


class EvidenceModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Evidence table."""

    __tablename__ = "evidence"

    attribution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("outcome_attributions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    content: Mapped[str] = mapped_column(String(10000), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    evidence_type: Mapped[str] = mapped_column(String(32), nullable=False, default="note")
```

### backend/app/infrastructure/persistence/models/notification.py

```python
"""ORM model for Notification."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class NotificationModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Notification table."""

    __tablename__ = "notifications"

    recipient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    body: Mapped[str] = mapped_column(String(4000), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    subject_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    subject_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    action_url: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(2000), nullable=True)
```

### backend/app/infrastructure/persistence/models/audit_log.py

```python
"""ORM model for AuditLog."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class AuditLogModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Audit log table."""

    __tablename__ = "audit_logs"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    resource_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    changes: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    audit_metadata: Mapped[dict] = mapped_column(
        "metadata", JSONB, nullable=False, default=dict
    )
```

### backend/app/infrastructure/persistence/mappers.py

```python
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
```

### backend/app/infrastructure/persistence/repositories/__init__.py

```python
"""SQLAlchemy repository implementations."""

from app.infrastructure.persistence.repositories.attribution_repository import (
    SQLAlchemyAttributionRepository,
    SQLAlchemyEvidenceRepository,
)
from app.infrastructure.persistence.repositories.audit_log_repository import (
    SQLAlchemyAuditLogRepository,
)
from app.infrastructure.persistence.repositories.kpi_repository import (
    SQLAlchemyKPIRepository,
    SQLAlchemyMetricSnapshotRepository,
)
from app.infrastructure.persistence.repositories.notification_repository import (
    SQLAlchemyNotificationRepository,
)
from app.infrastructure.persistence.repositories.okr_repository import (
    SQLAlchemyKeyResultRepository,
    SQLAlchemyObjectiveRepository,
)
from app.infrastructure.persistence.repositories.organization_repository import (
    SQLAlchemyOrganizationRepository,
    SQLAlchemyTeamRepository,
)
from app.infrastructure.persistence.repositories.outcome_repository import (
    SQLAlchemyBusinessOutcomeRepository,
)
from app.infrastructure.persistence.repositories.project_repository import (
    SQLAlchemyProjectRepository,
)
from app.infrastructure.persistence.repositories.sprint_repository import (
    SQLAlchemySprintRepository,
)
from app.infrastructure.persistence.repositories.user_repository import (
    SQLAlchemyTeamMembershipRepository,
    SQLAlchemyUserRepository,
)
from app.infrastructure.persistence.repositories.work_item_repository import (
    SQLAlchemyWorkItemRepository,
)

__all__ = [
    "SQLAlchemyAttributionRepository",
    "SQLAlchemyAuditLogRepository",
    "SQLAlchemyBusinessOutcomeRepository",
    "SQLAlchemyEvidenceRepository",
    "SQLAlchemyKPIRepository",
    "SQLAlchemyKeyResultRepository",
    "SQLAlchemyMetricSnapshotRepository",
    "SQLAlchemyNotificationRepository",
    "SQLAlchemyObjectiveRepository",
    "SQLAlchemyOrganizationRepository",
    "SQLAlchemyProjectRepository",
    "SQLAlchemySprintRepository",
    "SQLAlchemyTeamMembershipRepository",
    "SQLAlchemyTeamRepository",
    "SQLAlchemyUserRepository",
    "SQLAlchemyWorkItemRepository",
]
```

### backend/app/infrastructure/persistence/repositories/_base.py

```python
"""Shared helpers for SQLAlchemy repositories."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Select, desc
from sqlalchemy.sql.elements import ColumnElement

from app.domain.repositories.specifications import PageRequest


def apply_pagination(
    stmt: Select[Any], page: PageRequest, order_column: ColumnElement[Any]
) -> Select[Any]:
    """Apply ordering, limit, and offset to a select statement."""
    order = desc(order_column) if page.descending else order_column
    return stmt.order_by(order).limit(page.limit).offset(page.offset)


def utcnow() -> datetime:
    """Return the current UTC datetime with timezone information."""
    return datetime.now(timezone.utc)
```

### backend/app/infrastructure/persistence/repositories/organization_repository.py

```python
"""SQLAlchemy implementations of Organization and Team repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.organization import Organization, Team
from app.domain.repositories.organization_repository import (
    OrganizationRepositoryContract,
    TeamRepositoryContract,
)
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.mappers import OrganizationMapper, TeamMapper
from app.infrastructure.persistence.models.organization import (
    OrganizationModel,
    TeamModel,
)
from app.infrastructure.persistence.models.user import TeamMembershipModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyOrganizationRepository(OrganizationRepositoryContract):
    """SQLAlchemy implementation of the Organization repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Organization | None:
        model = self._session.get(OrganizationModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return OrganizationMapper.to_entity(model)

    def add(self, entity: Organization) -> Organization:
        model = OrganizationMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return OrganizationMapper.to_entity(model)

    def update(self, entity: Organization) -> Organization:
        model = self._session.get(OrganizationModel, entity.id)
        if model is None:
            raise NotFoundError(f"Organization {entity.id} not found")
        OrganizationMapper.to_model(entity, model)
        self._session.flush()
        return OrganizationMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(OrganizationModel, entity_id)
        if model is None:
            raise NotFoundError(f"Organization {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).where(
            OrganizationModel.id == entity_id,
            OrganizationModel.deleted_at.is_(None),
        )
        return (self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_slug(self, slug: str) -> Organization | None:
        stmt = select(OrganizationModel).where(
            OrganizationModel.slug == slug.lower(),
            OrganizationModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return OrganizationMapper.to_entity(model) if model else None

    def get_by_billing_email(self, email: str) -> Organization | None:
        stmt = select(OrganizationModel).where(
            func.lower(OrganizationModel.billing_email) == email.lower(),
            OrganizationModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return OrganizationMapper.to_entity(model) if model else None

    def list_all(self, page: PageRequest) -> Sequence[Organization]:
        stmt = select(OrganizationModel).where(OrganizationModel.deleted_at.is_(None))
        stmt = apply_pagination(stmt, page, OrganizationModel.created_at)
        return [OrganizationMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_active(self, page: PageRequest) -> Sequence[Organization]:
        stmt = select(OrganizationModel).where(
            OrganizationModel.deleted_at.is_(None),
            OrganizationModel.is_active.is_(True),
        )
        stmt = apply_pagination(stmt, page, OrganizationModel.created_at)
        return [OrganizationMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self) -> int:
        stmt = select(func.count()).select_from(OrganizationModel).where(
            OrganizationModel.deleted_at.is_(None)
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        stmt = select(func.count()).select_from(OrganizationModel).where(
            OrganizationModel.slug == slug.lower(),
            OrganizationModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(OrganizationModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0


class SQLAlchemyTeamRepository(TeamRepositoryContract):
    """SQLAlchemy implementation of the Team repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Team | None:
        model = self._session.get(TeamModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return TeamMapper.to_entity(model)

    def add(self, entity: Team) -> Team:
        model = TeamMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return TeamMapper.to_entity(model)

    def update(self, entity: Team) -> Team:
        model = self._session.get(TeamModel, entity.id)
        if model is None:
            raise NotFoundError(f"Team {entity.id} not found")
        TeamMapper.to_model(entity, model)
        self._session.flush()
        return TeamMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(TeamModel, entity_id)
        if model is None:
            raise NotFoundError(f"Team {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(TeamModel).where(
            TeamModel.id == entity_id,
            TeamModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_slug(self, organization_id: UUID, slug: str) -> Team | None:
        stmt = select(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.slug == slug.lower(),
            TeamModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return TeamMapper.to_entity(model) if model else None

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Team]:
        stmt = select(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, TeamModel.created_at)
        return [TeamMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_user(self, user_id: UUID) -> Sequence[Team]:
        stmt = (
            select(TeamModel)
            .join(TeamMembershipModel, TeamMembershipModel.team_id == TeamModel.id)
            .where(
                TeamMembershipModel.user_id == user_id,
                TeamMembershipModel.deleted_at.is_(None),
                TeamModel.deleted_at.is_(None),
            )
            .order_by(TeamModel.name.asc())
        )
        return [TeamMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count_by_organization(self, organization_id: UUID) -> int:
        stmt = select(func.count()).select_from(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(TeamModel).where(
            TeamModel.organization_id == organization_id,
            TeamModel.slug == slug.lower(),
            TeamModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(TeamModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0
```

### backend/app/infrastructure/persistence/repositories/user_repository.py

```python
"""SQLAlchemy implementations of User and TeamMembership repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.user import TeamMembership, User
from app.domain.repositories.specifications import PageRequest
from app.domain.repositories.user_repository import (
    TeamMembershipRepositoryContract,
    UserRepositoryContract,
)
from app.infrastructure.persistence.mappers import (
    TeamMembershipMapper,
    UserMapper,
)
from app.infrastructure.persistence.models.user import (
    TeamMembershipModel,
    UserModel,
)
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyUserRepository(UserRepositoryContract):
    """SQLAlchemy implementation of the User repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> User | None:
        model = self._session.get(UserModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return UserMapper.to_entity(model)

    def add(self, entity: User) -> User:
        model = UserMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return UserMapper.to_entity(model)

    def update(self, entity: User) -> User:
        model = self._session.get(UserModel, entity.id)
        if model is None:
            raise NotFoundError(f"User {entity.id} not found")
        UserMapper.to_model(entity, model)
        self._session.flush()
        return UserMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(UserModel, entity_id)
        if model is None:
            raise NotFoundError(f"User {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(UserModel).where(
            UserModel.id == entity_id,
            UserModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(
            func.lower(UserModel.email) == email.lower(),
            UserModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    def email_exists(self, email: str, exclude_id: UUID | None = None) -> bool:
        stmt = select(func.count()).select_from(UserModel).where(
            func.lower(UserModel.email) == email.lower(),
            UserModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(UserModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[User]:
        stmt = select(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, UserModel.created_at)
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_team(self, team_id: UUID) -> Sequence[User]:
        stmt = (
            select(UserModel)
            .join(TeamMembershipModel, TeamMembershipModel.user_id == UserModel.id)
            .where(
                TeamMembershipModel.team_id == team_id,
                TeamMembershipModel.deleted_at.is_(None),
                UserModel.deleted_at.is_(None),
            )
            .order_by(UserModel.full_name.asc())
        )
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_role(
        self, organization_id: UUID, role: str, page: PageRequest
    ) -> Sequence[User]:
        stmt = select(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.role == role,
            UserModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, UserModel.created_at)
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def search(
        self, organization_id: UUID, query: str, page: PageRequest
    ) -> Sequence[User]:
        pattern = f"%{query.lower()}%"
        stmt = select(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.deleted_at.is_(None),
            or_(
                func.lower(UserModel.email).like(pattern),
                func.lower(UserModel.full_name).like(pattern),
            ),
        )
        stmt = apply_pagination(stmt, page, UserModel.full_name)
        return [UserMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count_by_organization(self, organization_id: UUID) -> int:
        stmt = select(func.count()).select_from(UserModel).where(
            UserModel.organization_id == organization_id,
            UserModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)


class SQLAlchemyTeamMembershipRepository(TeamMembershipRepositoryContract):
    """SQLAlchemy implementation of the TeamMembership repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> TeamMembership | None:
        model = self._session.get(TeamMembershipModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return TeamMembershipMapper.to_entity(model)

    def add(self, entity: TeamMembership) -> TeamMembership:
        model = TeamMembershipMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return TeamMembershipMapper.to_entity(model)

    def update(self, entity: TeamMembership) -> TeamMembership:
        model = self._session.get(TeamMembershipModel, entity.id)
        if model is None:
            raise NotFoundError(f"TeamMembership {entity.id} not found")
        TeamMembershipMapper.to_model(entity, model)
        self._session.flush()
        return TeamMembershipMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(TeamMembershipModel, entity_id)
        if model is None:
            raise NotFoundError(f"TeamMembership {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(TeamMembershipModel).where(
            TeamMembershipModel.id == entity_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_team_and_user(
        self, team_id: UUID, user_id: UUID
    ) -> TeamMembership | None:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.team_id == team_id,
            TeamMembershipModel.user_id == user_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return TeamMembershipMapper.to_entity(model) if model else None

    def list_by_team(self, team_id: UUID) -> Sequence[TeamMembership]:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.team_id == team_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        return [
            TeamMembershipMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_user(self, user_id: UUID) -> Sequence[TeamMembership]:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.user_id == user_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        return [
            TeamMembershipMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def remove_by_team_and_user(self, team_id: UUID, user_id: UUID) -> None:
        stmt = select(TeamMembershipModel).where(
            TeamMembershipModel.team_id == team_id,
            TeamMembershipModel.user_id == user_id,
            TeamMembershipModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        if model is None:
            raise NotFoundError("Team membership not found")
        model.deleted_at = utcnow()
        self._session.flush()
```

### backend/app/infrastructure/persistence/repositories/project_repository.py

```python
"""SQLAlchemy implementation of the Project repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.project import Project
from app.domain.repositories.project_repository import ProjectRepositoryContract
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.mappers import ProjectMapper
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyProjectRepository(ProjectRepositoryContract):
    """SQLAlchemy implementation of the Project repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Project | None:
        model = self._session.get(ProjectModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return ProjectMapper.to_entity(model)

    def add(self, entity: Project) -> Project:
        model = ProjectMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return ProjectMapper.to_entity(model)

    def update(self, entity: Project) -> Project:
        model = self._session.get(ProjectModel, entity.id)
        if model is None:
            raise NotFoundError(f"Project {entity.id} not found")
        ProjectMapper.to_model(entity, model)
        self._session.flush()
        return ProjectMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(ProjectModel, entity_id)
        if model is None:
            raise NotFoundError(f"Project {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.id == entity_id,
            ProjectModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_key(self, organization_id: UUID, key: str) -> Project | None:
        stmt = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.key == key.upper(),
            ProjectModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return ProjectMapper.to_entity(model) if model else None

    def get_by_slug(self, organization_id: UUID, slug: str) -> Project | None:
        stmt = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.slug == slug.lower(),
            ProjectModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return ProjectMapper.to_entity(model) if model else None

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        stmt = select(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.deleted_at.is_(None),
        )
        if not include_archived:
            stmt = stmt.where(ProjectModel.is_archived.is_(False))
        stmt = apply_pagination(stmt, page, ProjectModel.created_at)
        return [ProjectMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_team(
        self, team_id: UUID, page: PageRequest, include_archived: bool = False
    ) -> Sequence[Project]:
        stmt = select(ProjectModel).where(
            ProjectModel.team_id == team_id,
            ProjectModel.deleted_at.is_(None),
        )
        if not include_archived:
            stmt = stmt.where(ProjectModel.is_archived.is_(False))
        stmt = apply_pagination(stmt, page, ProjectModel.created_at)
        return [ProjectMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def key_exists(
        self, organization_id: UUID, key: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.key == key.upper(),
            ProjectModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(ProjectModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def slug_exists(
        self, organization_id: UUID, slug: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.slug == slug.lower(),
            ProjectModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(ProjectModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def count_by_organization(
        self, organization_id: UUID, include_archived: bool = False
    ) -> int:
        stmt = select(func.count()).select_from(ProjectModel).where(
            ProjectModel.organization_id == organization_id,
            ProjectModel.deleted_at.is_(None),
        )
        if not include_archived:
            stmt = stmt.where(ProjectModel.is_archived.is_(False))
        return int(self._session.execute(stmt).scalar_one() or 0)
```

### backend/app/infrastructure/persistence/repositories/sprint_repository.py

```python
"""SQLAlchemy implementation of the Sprint repository."""

from __future__ import annotations

from datetime import date
from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.sprint import Sprint
from app.domain.enums import SprintStatus
from app.domain.repositories.specifications import PageRequest, SprintFilter
from app.domain.repositories.sprint_repository import SprintRepositoryContract
from app.infrastructure.persistence.mappers import SprintMapper
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.models.sprint import SprintModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemySprintRepository(SprintRepositoryContract):
    """SQLAlchemy implementation of the Sprint repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Sprint | None:
        model = self._session.get(SprintModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return SprintMapper.to_entity(model)

    def add(self, entity: Sprint) -> Sprint:
        model = SprintMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return SprintMapper.to_entity(model)

    def update(self, entity: Sprint) -> Sprint:
        model = self._session.get(SprintModel, entity.id)
        if model is None:
            raise NotFoundError(f"Sprint {entity.id} not found")
        SprintMapper.to_model(entity, model)
        self._session.flush()
        return SprintMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(SprintModel, entity_id)
        if model is None:
            raise NotFoundError(f"Sprint {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(SprintModel).where(
            SprintModel.id == entity_id,
            SprintModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_project(self, project_id: UUID, page: PageRequest) -> Sequence[Sprint]:
        stmt = select(SprintModel).where(
            SprintModel.project_id == project_id,
            SprintModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, SprintModel.start_date)
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def get_active_for_project(self, project_id: UUID) -> Sprint | None:
        stmt = select(SprintModel).where(
            SprintModel.project_id == project_id,
            SprintModel.status == SprintStatus.ACTIVE.value,
            SprintModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return SprintMapper.to_entity(model) if model else None

    def list_completed_in_range(
        self, organization_id: UUID, start: date, end: date
    ) -> Sequence[Sprint]:
        stmt = (
            select(SprintModel)
            .join(ProjectModel, ProjectModel.id == SprintModel.project_id)
            .where(
                ProjectModel.organization_id == organization_id,
                SprintModel.status == SprintStatus.COMPLETED.value,
                SprintModel.end_date >= start,
                SprintModel.end_date <= end,
                SprintModel.deleted_at.is_(None),
            )
            .order_by(SprintModel.end_date.desc())
        )
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_active_for_organization(
        self, organization_id: UUID
    ) -> Sequence[Sprint]:
        stmt = (
            select(SprintModel)
            .join(ProjectModel, ProjectModel.id == SprintModel.project_id)
            .where(
                ProjectModel.organization_id == organization_id,
                SprintModel.status == SprintStatus.ACTIVE.value,
                SprintModel.deleted_at.is_(None),
            )
            .order_by(SprintModel.start_date.desc())
        )
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: SprintFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.join(ProjectModel, ProjectModel.id == SprintModel.project_id).where(
                ProjectModel.organization_id == spec.organization_id
            )
        if spec.project_id:
            stmt = stmt.where(SprintModel.project_id == spec.project_id)
        if spec.statuses:
            stmt = stmt.where(SprintModel.status.in_(spec.statuses))
        if spec.starts_after:
            stmt = stmt.where(SprintModel.start_date >= spec.starts_after)
        if spec.ends_before:
            stmt = stmt.where(SprintModel.end_date <= spec.ends_before)
        if not spec.include_deleted:
            stmt = stmt.where(SprintModel.deleted_at.is_(None))
        return stmt

    def find(self, spec: SprintFilter, page: PageRequest) -> Sequence[Sprint]:
        stmt = self._apply_filter(select(SprintModel), spec)
        stmt = apply_pagination(stmt, page, SprintModel.start_date)
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: SprintFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(SprintModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)

    def latest_by_project(self, project_id: UUID, limit: int = 5) -> Sequence[Sprint]:
        if limit <= 0:
            return []
        stmt = (
            select(SprintModel)
            .where(
                SprintModel.project_id == project_id,
                SprintModel.deleted_at.is_(None),
            )
            .order_by(SprintModel.start_date.desc())
            .limit(limit)
        )
        return [SprintMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]
```

### backend/app/infrastructure/persistence/repositories/work_item_repository.py

```python
"""SQLAlchemy implementation of the WorkItem repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select, update
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.work_item import WorkItem
from app.domain.enums import WorkItemStatus
from app.domain.repositories.specifications import PageRequest, WorkItemFilter
from app.domain.repositories.work_item_repository import WorkItemRepositoryContract
from app.infrastructure.persistence.mappers import WorkItemMapper
from app.infrastructure.persistence.models.attribution import OutcomeAttributionModel
from app.infrastructure.persistence.models.project import ProjectModel
from app.infrastructure.persistence.models.work_item import WorkItemModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyWorkItemRepository(WorkItemRepositoryContract):
    """SQLAlchemy implementation of the WorkItem repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> WorkItem | None:
        model = self._session.get(WorkItemModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return WorkItemMapper.to_entity(model)

    def add(self, entity: WorkItem) -> WorkItem:
        model = WorkItemMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return WorkItemMapper.to_entity(model)

    def update(self, entity: WorkItem) -> WorkItem:
        model = self._session.get(WorkItemModel, entity.id)
        if model is None:
            raise NotFoundError(f"WorkItem {entity.id} not found")
        WorkItemMapper.to_model(entity, model)
        self._session.flush()
        return WorkItemMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(WorkItemModel, entity_id)
        if model is None:
            raise NotFoundError(f"WorkItem {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(WorkItemModel).where(
            WorkItemModel.id == entity_id,
            WorkItemModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_external_key(
        self, project_id: UUID, external_key: str
    ) -> WorkItem | None:
        stmt = select(WorkItemModel).where(
            WorkItemModel.project_id == project_id,
            WorkItemModel.external_key == external_key,
            WorkItemModel.deleted_at.is_(None),
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return WorkItemMapper.to_entity(model) if model else None

    def list_by_sprint(self, sprint_id: UUID) -> Sequence[WorkItem]:
        stmt = (
            select(WorkItemModel)
            .where(
                WorkItemModel.sprint_id == sprint_id,
                WorkItemModel.deleted_at.is_(None),
            )
            .order_by(WorkItemModel.created_at.desc())
        )
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_project(
        self, project_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        stmt = select(WorkItemModel).where(
            WorkItemModel.project_id == project_id,
            WorkItemModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, WorkItemModel.created_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_epic(self, epic_id: UUID) -> Sequence[WorkItem]:
        stmt = (
            select(WorkItemModel)
            .where(
                WorkItemModel.epic_id == epic_id,
                WorkItemModel.deleted_at.is_(None),
            )
            .order_by(WorkItemModel.created_at.desc())
        )
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_parent(self, parent_id: UUID) -> Sequence[WorkItem]:
        stmt = (
            select(WorkItemModel)
            .where(
                WorkItemModel.parent_id == parent_id,
                WorkItemModel.deleted_at.is_(None),
            )
            .order_by(WorkItemModel.created_at.desc())
        )
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_assignee(
        self, user_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        stmt = select(WorkItemModel).where(
            WorkItemModel.assignee_id == user_id,
            WorkItemModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, WorkItemModel.created_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_unattributed(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[WorkItem]:
        subq = (
            select(OutcomeAttributionModel.work_item_id)
            .where(
                OutcomeAttributionModel.work_item_id.is_not(None),
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .subquery()
        )
        stmt = (
            select(WorkItemModel)
            .join(ProjectModel, ProjectModel.id == WorkItemModel.project_id)
            .where(
                ProjectModel.organization_id == organization_id,
                WorkItemModel.status == WorkItemStatus.DONE.value,
                WorkItemModel.deleted_at.is_(None),
                WorkItemModel.id.not_in(select(subq.c.work_item_id)),
            )
        )
        stmt = apply_pagination(stmt, page, WorkItemModel.completed_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: WorkItemFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.join(ProjectModel, ProjectModel.id == WorkItemModel.project_id).where(
                ProjectModel.organization_id == spec.organization_id
            )
        if spec.project_id:
            stmt = stmt.where(WorkItemModel.project_id == spec.project_id)
        if spec.sprint_id:
            stmt = stmt.where(WorkItemModel.sprint_id == spec.sprint_id)
        if spec.assignee_id:
            stmt = stmt.where(WorkItemModel.assignee_id == spec.assignee_id)
        if spec.reporter_id:
            stmt = stmt.where(WorkItemModel.reporter_id == spec.reporter_id)
        if spec.epic_id:
            stmt = stmt.where(WorkItemModel.epic_id == spec.epic_id)
        if spec.item_types:
            stmt = stmt.where(WorkItemModel.item_type.in_(spec.item_types))
        if spec.statuses:
            stmt = stmt.where(WorkItemModel.status.in_(spec.statuses))
        if spec.priorities:
            stmt = stmt.where(WorkItemModel.priority.in_(spec.priorities))
        if spec.labels:
            stmt = stmt.where(WorkItemModel.labels.op("&&")(list(spec.labels)))
        if spec.search:
            pattern = f"%{spec.search.lower()}%"
            stmt = stmt.where(func.lower(WorkItemModel.title).like(pattern))
        if spec.completed_after:
            stmt = stmt.where(WorkItemModel.completed_at >= spec.completed_after)
        if spec.completed_before:
            stmt = stmt.where(WorkItemModel.completed_at <= spec.completed_before)
        if not spec.include_deleted:
            stmt = stmt.where(WorkItemModel.deleted_at.is_(None))
        return stmt

    def find(self, spec: WorkItemFilter, page: PageRequest) -> Sequence[WorkItem]:
        stmt = self._apply_filter(select(WorkItemModel), spec)
        stmt = apply_pagination(stmt, page, WorkItemModel.created_at)
        return [WorkItemMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: WorkItemFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(WorkItemModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)

    def bulk_reassign_sprint(
        self, work_item_ids: Sequence[UUID], sprint_id: UUID | None
    ) -> int:
        if not work_item_ids:
            return 0
        stmt = (
            update(WorkItemModel)
            .where(
                WorkItemModel.id.in_(list(work_item_ids)),
                WorkItemModel.deleted_at.is_(None),
            )
            .values(sprint_id=sprint_id, updated_at=utcnow())
        )
        result = self._session.execute(stmt)
        return int(result.rowcount or 0)
```

### backend/app/infrastructure/persistence/repositories/outcome_repository.py

```python
"""SQLAlchemy implementation of the BusinessOutcome repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.enums import OutcomeStatus
from app.domain.repositories.outcome_repository import (
    BusinessOutcomeRepositoryContract,
)
from app.domain.repositories.specifications import OutcomeFilter, PageRequest
from app.infrastructure.persistence.mappers import BusinessOutcomeMapper
from app.infrastructure.persistence.models.business_outcome import BusinessOutcomeModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyBusinessOutcomeRepository(BusinessOutcomeRepositoryContract):
    """SQLAlchemy implementation of the BusinessOutcome repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> BusinessOutcome | None:
        model = self._session.get(BusinessOutcomeModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return BusinessOutcomeMapper.to_entity(model)

    def add(self, entity: BusinessOutcome) -> BusinessOutcome:
        model = BusinessOutcomeMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return BusinessOutcomeMapper.to_entity(model)

    def update(self, entity: BusinessOutcome) -> BusinessOutcome:
        model = self._session.get(BusinessOutcomeModel, entity.id)
        if model is None:
            raise NotFoundError(f"BusinessOutcome {entity.id} not found")
        BusinessOutcomeMapper.to_model(entity, model)
        self._session.flush()
        return BusinessOutcomeMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(BusinessOutcomeModel, entity_id)
        if model is None:
            raise NotFoundError(f"BusinessOutcome {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(BusinessOutcomeModel).where(
            BusinessOutcomeModel.id == entity_id,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = select(BusinessOutcomeModel).where(
            BusinessOutcomeModel.organization_id == organization_id,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = select(BusinessOutcomeModel).where(
            BusinessOutcomeModel.owner_id == owner_id,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_off_track(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        stmt = (
            select(BusinessOutcomeModel)
            .where(
                BusinessOutcomeModel.organization_id == organization_id,
                BusinessOutcomeModel.status == OutcomeStatus.OFF_TRACK.value,
                BusinessOutcomeModel.deleted_at.is_(None),
            )
            .order_by(BusinessOutcomeModel.target_date.asc().nulls_last())
        )
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_at_risk(self, organization_id: UUID) -> Sequence[BusinessOutcome]:
        stmt = (
            select(BusinessOutcomeModel)
            .where(
                BusinessOutcomeModel.organization_id == organization_id,
                BusinessOutcomeModel.status == OutcomeStatus.AT_RISK.value,
                BusinessOutcomeModel.deleted_at.is_(None),
            )
            .order_by(BusinessOutcomeModel.target_date.asc().nulls_last())
        )
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = select(BusinessOutcomeModel).where(
            BusinessOutcomeModel.organization_id == organization_id,
            BusinessOutcomeModel.status == OutcomeStatus.ACTIVE.value,
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def _apply_filter(self, stmt: Select, spec: OutcomeFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(BusinessOutcomeModel.organization_id == spec.organization_id)
        if spec.owner_id:
            stmt = stmt.where(BusinessOutcomeModel.owner_id == spec.owner_id)
        if spec.statuses:
            stmt = stmt.where(BusinessOutcomeModel.status.in_(spec.statuses))
        if spec.target_before:
            stmt = stmt.where(BusinessOutcomeModel.target_date <= spec.target_before)
        if spec.target_after:
            stmt = stmt.where(BusinessOutcomeModel.target_date >= spec.target_after)
        if spec.search:
            pattern = f"%{spec.search.lower()}%"
            stmt = stmt.where(func.lower(BusinessOutcomeModel.name).like(pattern))
        if not spec.include_deleted:
            stmt = stmt.where(BusinessOutcomeModel.deleted_at.is_(None))
        return stmt

    def find(
        self, spec: OutcomeFilter, page: PageRequest
    ) -> Sequence[BusinessOutcome]:
        stmt = self._apply_filter(select(BusinessOutcomeModel), spec)
        stmt = apply_pagination(stmt, page, BusinessOutcomeModel.created_at)
        return [
            BusinessOutcomeMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count(self, spec: OutcomeFilter) -> int:
        stmt = self._apply_filter(
            select(func.count()).select_from(BusinessOutcomeModel), spec
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(BusinessOutcomeModel).where(
            BusinessOutcomeModel.organization_id == organization_id,
            func.lower(BusinessOutcomeModel.name) == name.lower(),
            BusinessOutcomeModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(BusinessOutcomeModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0
```

================================================================================

### backend/app/infrastructure/persistence/repositories/kpi_repository.py

```python
"""SQLAlchemy implementations of KPI and MetricSnapshot repositories."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, delete, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.kpi import KPI, MetricSnapshot
from app.domain.repositories.kpi_repository import (
    KPIRepositoryContract,
    MetricSnapshotRepositoryContract,
)
from app.domain.repositories.specifications import (
    KPIFilter,
    MetricSnapshotFilter,
    PageRequest,
)
from app.infrastructure.persistence.mappers import KPIMapper, MetricSnapshotMapper
from app.infrastructure.persistence.models.kpi import KPIModel, MetricSnapshotModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyKPIRepository(KPIRepositoryContract):
    """SQLAlchemy implementation of the KPI repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> KPI | None:
        model = self._session.get(KPIModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return KPIMapper.to_entity(model)

    def add(self, entity: KPI) -> KPI:
        model = KPIMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return KPIMapper.to_entity(model)

    def update(self, entity: KPI) -> KPI:
        model = self._session.get(KPIModel, entity.id)
        if model is None:
            raise NotFoundError(f"KPI {entity.id} not found")
        KPIMapper.to_model(entity, model)
        self._session.flush()
        return KPIMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(KPIModel, entity_id)
        if model is None:
            raise NotFoundError(f"KPI {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(KPIModel).where(
            KPIModel.id == entity_id,
            KPIModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.organization_id == organization_id,
            KPIModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_outcome(self, outcome_id: UUID) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.outcome_id == outcome_id,
            KPIModel.deleted_at.is_(None),
        ).order_by(KPIModel.name.asc())
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_owner(self, owner_id: UUID, page: PageRequest) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.owner_id == owner_id,
            KPIModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_active(self, organization_id: UUID, page: PageRequest) -> Sequence[KPI]:
        stmt = select(KPIModel).where(
            KPIModel.organization_id == organization_id,
            KPIModel.is_active.is_(True),
            KPIModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: KPIFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(KPIModel.organization_id == spec.organization_id)
        if spec.outcome_id:
            stmt = stmt.where(KPIModel.outcome_id == spec.outcome_id)
        if spec.owner_id:
            stmt = stmt.where(KPIModel.owner_id == spec.owner_id)
        if spec.units:
            stmt = stmt.where(KPIModel.unit.in_(spec.units))
        if spec.is_active is not None:
            stmt = stmt.where(KPIModel.is_active.is_(spec.is_active))
        if not spec.include_deleted:
            stmt = stmt.where(KPIModel.deleted_at.is_(None))
        return stmt

    def find(self, spec: KPIFilter, page: PageRequest) -> Sequence[KPI]:
        stmt = self._apply_filter(select(KPIModel), spec)
        stmt = apply_pagination(stmt, page, KPIModel.created_at)
        return [KPIMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: KPIFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(KPIModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)

    def name_exists(
        self, organization_id: UUID, name: str, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(KPIModel).where(
            KPIModel.organization_id == organization_id,
            func.lower(KPIModel.name) == name.lower(),
            KPIModel.deleted_at.is_(None),
        )
        if exclude_id is not None:
            stmt = stmt.where(KPIModel.id != exclude_id)
        return int(self._session.execute(stmt).scalar_one() or 0) > 0


class SQLAlchemyMetricSnapshotRepository(MetricSnapshotRepositoryContract):
    """SQLAlchemy implementation of the MetricSnapshot repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> MetricSnapshot | None:
        model = self._session.get(MetricSnapshotModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return MetricSnapshotMapper.to_entity(model)

    def add(self, entity: MetricSnapshot) -> MetricSnapshot:
        model = MetricSnapshotMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return MetricSnapshotMapper.to_entity(model)

    def update(self, entity: MetricSnapshot) -> MetricSnapshot:
        model = self._session.get(MetricSnapshotModel, entity.id)
        if model is None:
            raise NotFoundError(f"MetricSnapshot {entity.id} not found")
        MetricSnapshotMapper.to_model(entity, model)
        self._session.flush()
        return MetricSnapshotMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(MetricSnapshotModel, entity_id)
        if model is None:
            raise NotFoundError(f"MetricSnapshot {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(MetricSnapshotModel).where(
            MetricSnapshotModel.id == entity_id,
            MetricSnapshotModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_kpi(
        self, kpi_id: UUID, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        stmt = select(MetricSnapshotModel).where(
            MetricSnapshotModel.kpi_id == kpi_id,
            MetricSnapshotModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, MetricSnapshotModel.recorded_at)
        return [
            MetricSnapshotMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def latest_for_kpi(self, kpi_id: UUID) -> MetricSnapshot | None:
        stmt = (
            select(MetricSnapshotModel)
            .where(
                MetricSnapshotModel.kpi_id == kpi_id,
                MetricSnapshotModel.deleted_at.is_(None),
            )
            .order_by(MetricSnapshotModel.recorded_at.desc())
            .limit(1)
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return MetricSnapshotMapper.to_entity(model) if model else None

    def list_in_range(
        self, kpi_id: UUID, start: datetime, end: datetime
    ) -> Sequence[MetricSnapshot]:
        stmt = (
            select(MetricSnapshotModel)
            .where(
                MetricSnapshotModel.kpi_id == kpi_id,
                MetricSnapshotModel.recorded_at >= start,
                MetricSnapshotModel.recorded_at <= end,
                MetricSnapshotModel.deleted_at.is_(None),
            )
            .order_by(MetricSnapshotModel.recorded_at.asc())
        )
        return [
            MetricSnapshotMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def find(
        self, spec: MetricSnapshotFilter, page: PageRequest
    ) -> Sequence[MetricSnapshot]:
        stmt = select(MetricSnapshotModel).where(MetricSnapshotModel.deleted_at.is_(None))
        if spec.kpi_id:
            stmt = stmt.where(MetricSnapshotModel.kpi_id == spec.kpi_id)
        if spec.recorded_after:
            stmt = stmt.where(MetricSnapshotModel.recorded_at >= spec.recorded_after)
        if spec.recorded_before:
            stmt = stmt.where(MetricSnapshotModel.recorded_at <= spec.recorded_before)
        if spec.source:
            stmt = stmt.where(MetricSnapshotModel.source == spec.source)
        stmt = apply_pagination(stmt, page, MetricSnapshotModel.recorded_at)
        return [
            MetricSnapshotMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def delete_older_than(self, kpi_id: UUID, cutoff: datetime) -> int:
        stmt = delete(MetricSnapshotModel).where(
            MetricSnapshotModel.kpi_id == kpi_id,
            MetricSnapshotModel.recorded_at < cutoff,
        )
        result = self._session.execute(stmt)
        return int(result.rowcount or 0)
```

### backend/app/infrastructure/persistence/repositories/okr_repository.py

```python
"""SQLAlchemy implementations of Objective and KeyResult repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.okr import KeyResult, Objective
from app.domain.enums import OKRStatus
from app.domain.repositories.okr_repository import (
    KeyResultRepositoryContract,
    ObjectiveRepositoryContract,
)
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.mappers import KeyResultMapper, ObjectiveMapper
from app.infrastructure.persistence.models.okr import KeyResultModel, ObjectiveModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyObjectiveRepository(ObjectiveRepositoryContract):
    """SQLAlchemy implementation of the Objective repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Objective | None:
        model = self._session.get(ObjectiveModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return ObjectiveMapper.to_entity(model)

    def add(self, entity: Objective) -> Objective:
        model = ObjectiveMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return ObjectiveMapper.to_entity(model)

    def update(self, entity: Objective) -> Objective:
        model = self._session.get(ObjectiveModel, entity.id)
        if model is None:
            raise NotFoundError(f"Objective {entity.id} not found")
        ObjectiveMapper.to_model(entity, model)
        self._session.flush()
        return ObjectiveMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(ObjectiveModel, entity_id)
        if model is None:
            raise NotFoundError(f"Objective {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(ObjectiveModel).where(
            ObjectiveModel.id == entity_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.organization_id == organization_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_team(
        self, team_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.team_id == team_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_owner(
        self, owner_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.owner_id == owner_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_parent(self, parent_id: UUID) -> Sequence[Objective]:
        stmt = (
            select(ObjectiveModel)
            .where(
                ObjectiveModel.parent_id == parent_id,
                ObjectiveModel.deleted_at.is_(None),
            )
            .order_by(ObjectiveModel.created_at.desc())
        )
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_active(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[Objective]:
        stmt = select(ObjectiveModel).where(
            ObjectiveModel.organization_id == organization_id,
            ObjectiveModel.status == OKRStatus.ACTIVE.value,
            ObjectiveModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, ObjectiveModel.created_at)
        return [
            ObjectiveMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_by_organization(self, organization_id: UUID) -> int:
        stmt = select(func.count()).select_from(ObjectiveModel).where(
            ObjectiveModel.organization_id == organization_id,
            ObjectiveModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)


class SQLAlchemyKeyResultRepository(KeyResultRepositoryContract):
    """SQLAlchemy implementation of the KeyResult repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> KeyResult | None:
        model = self._session.get(KeyResultModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return KeyResultMapper.to_entity(model)

    def add(self, entity: KeyResult) -> KeyResult:
        model = KeyResultMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return KeyResultMapper.to_entity(model)

    def update(self, entity: KeyResult) -> KeyResult:
        model = self._session.get(KeyResultModel, entity.id)
        if model is None:
            raise NotFoundError(f"KeyResult {entity.id} not found")
        KeyResultMapper.to_model(entity, model)
        self._session.flush()
        return KeyResultMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(KeyResultModel, entity_id)
        if model is None:
            raise NotFoundError(f"KeyResult {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(KeyResultModel).where(
            KeyResultModel.id == entity_id,
            KeyResultModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_objective(self, objective_id: UUID) -> Sequence[KeyResult]:
        stmt = (
            select(KeyResultModel)
            .where(
                KeyResultModel.objective_id == objective_id,
                KeyResultModel.deleted_at.is_(None),
            )
            .order_by(KeyResultModel.created_at.asc())
        )
        return [
            KeyResultMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_kpi(self, kpi_id: UUID) -> Sequence[KeyResult]:
        stmt = (
            select(KeyResultModel)
            .where(
                KeyResultModel.kpi_id == kpi_id,
                KeyResultModel.deleted_at.is_(None),
            )
            .order_by(KeyResultModel.created_at.asc())
        )
        return [
            KeyResultMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_by_objective(self, objective_id: UUID) -> int:
        stmt = select(func.count()).select_from(KeyResultModel).where(
            KeyResultModel.objective_id == objective_id,
            KeyResultModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def delete_by_objective(self, objective_id: UUID) -> int:
        now = utcnow()
        stmt = (
            select(KeyResultModel)
            .where(
                KeyResultModel.objective_id == objective_id,
                KeyResultModel.deleted_at.is_(None),
            )
        )
        models = list(self._session.execute(stmt).scalars())
        for model in models:
            model.deleted_at = now
        self._session.flush()
        return len(models)
```

### backend/app/infrastructure/persistence/repositories/attribution_repository.py

```python
"""SQLAlchemy implementations of Attribution and Evidence repositories."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.attribution import Evidence, OutcomeAttribution
from app.domain.repositories.attribution_repository import (
    AttributionRepositoryContract,
    EvidenceRepositoryContract,
)
from app.domain.repositories.specifications import AttributionFilter, PageRequest
from app.infrastructure.persistence.mappers import AttributionMapper, EvidenceMapper
from app.infrastructure.persistence.models.attribution import (
    EvidenceModel,
    OutcomeAttributionModel,
)
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyAttributionRepository(AttributionRepositoryContract):
    """SQLAlchemy implementation of the OutcomeAttribution repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> OutcomeAttribution | None:
        model = self._session.get(OutcomeAttributionModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return AttributionMapper.to_entity(model)

    def add(self, entity: OutcomeAttribution) -> OutcomeAttribution:
        model = AttributionMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return AttributionMapper.to_entity(model)

    def update(self, entity: OutcomeAttribution) -> OutcomeAttribution:
        model = self._session.get(OutcomeAttributionModel, entity.id)
        if model is None:
            raise NotFoundError(f"Attribution {entity.id} not found")
        AttributionMapper.to_model(entity, model)
        self._session.flush()
        return AttributionMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(OutcomeAttributionModel, entity_id)
        if model is None:
            raise NotFoundError(f"Attribution {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(OutcomeAttributionModel).where(
            OutcomeAttributionModel.id == entity_id,
            OutcomeAttributionModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_work_item(self, work_item_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.work_item_id == work_item_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_sprint(self, sprint_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.sprint_id == sprint_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_outcome(self, outcome_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.outcome_id == outcome_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_kpi(self, kpi_id: UUID) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.kpi_id == kpi_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_key_result(
        self, key_result_id: UUID
    ) -> Sequence[OutcomeAttribution]:
        stmt = (
            select(OutcomeAttributionModel)
            .where(
                OutcomeAttributionModel.key_result_id == key_result_id,
                OutcomeAttributionModel.deleted_at.is_(None),
            )
            .order_by(OutcomeAttributionModel.created_at.desc())
        )
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        stmt = select(OutcomeAttributionModel).where(
            OutcomeAttributionModel.organization_id == organization_id,
            OutcomeAttributionModel.deleted_at.is_(None),
        )
        stmt = apply_pagination(stmt, page, OutcomeAttributionModel.created_at)
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def _apply_filter(self, stmt: Select, spec: AttributionFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(OutcomeAttributionModel.organization_id == spec.organization_id)
        if spec.work_item_id:
            stmt = stmt.where(OutcomeAttributionModel.work_item_id == spec.work_item_id)
        if spec.sprint_id:
            stmt = stmt.where(OutcomeAttributionModel.sprint_id == spec.sprint_id)
        if spec.outcome_id:
            stmt = stmt.where(OutcomeAttributionModel.outcome_id == spec.outcome_id)
        if spec.kpi_id:
            stmt = stmt.where(OutcomeAttributionModel.kpi_id == spec.kpi_id)
        if spec.key_result_id:
            stmt = stmt.where(OutcomeAttributionModel.key_result_id == spec.key_result_id)
        if spec.strengths:
            stmt = stmt.where(OutcomeAttributionModel.strength.in_(spec.strengths))
        if spec.methods:
            stmt = stmt.where(OutcomeAttributionModel.method.in_(spec.methods))
        if not spec.include_deleted:
            stmt = stmt.where(OutcomeAttributionModel.deleted_at.is_(None))
        return stmt

    def find(
        self, spec: AttributionFilter, page: PageRequest
    ) -> Sequence[OutcomeAttribution]:
        stmt = self._apply_filter(select(OutcomeAttributionModel), spec)
        stmt = apply_pagination(stmt, page, OutcomeAttributionModel.created_at)
        return [
            AttributionMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count(self, spec: AttributionFilter) -> int:
        stmt = self._apply_filter(
            select(func.count()).select_from(OutcomeAttributionModel), spec
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def exists_for_pair(
        self,
        work_item_id: UUID | None,
        sprint_id: UUID | None,
        outcome_id: UUID | None,
        kpi_id: UUID | None,
        key_result_id: UUID | None,
    ) -> bool:
        stmt = select(func.count()).select_from(OutcomeAttributionModel).where(
            OutcomeAttributionModel.deleted_at.is_(None)
        )
        stmt = stmt.where(
            OutcomeAttributionModel.work_item_id.is_(None)
            if work_item_id is None
            else OutcomeAttributionModel.work_item_id == work_item_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.sprint_id.is_(None)
            if sprint_id is None
            else OutcomeAttributionModel.sprint_id == sprint_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.outcome_id.is_(None)
            if outcome_id is None
            else OutcomeAttributionModel.outcome_id == outcome_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.kpi_id.is_(None)
            if kpi_id is None
            else OutcomeAttributionModel.kpi_id == kpi_id
        )
        stmt = stmt.where(
            OutcomeAttributionModel.key_result_id.is_(None)
            if key_result_id is None
            else OutcomeAttributionModel.key_result_id == key_result_id
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0


class SQLAlchemyEvidenceRepository(EvidenceRepositoryContract):
    """SQLAlchemy implementation of the Evidence repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Evidence | None:
        model = self._session.get(EvidenceModel, entity_id)
        if model is None or model.deleted_at is not None:
            return None
        return EvidenceMapper.to_entity(model)

    def add(self, entity: Evidence) -> Evidence:
        model = EvidenceMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return EvidenceMapper.to_entity(model)

    def update(self, entity: Evidence) -> Evidence:
        model = self._session.get(EvidenceModel, entity.id)
        if model is None:
            raise NotFoundError(f"Evidence {entity.id} not found")
        EvidenceMapper.to_model(entity, model)
        self._session.flush()
        return EvidenceMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(EvidenceModel, entity_id)
        if model is None:
            raise NotFoundError(f"Evidence {entity_id} not found")
        model.deleted_at = utcnow()
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(EvidenceModel).where(
            EvidenceModel.id == entity_id,
            EvidenceModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_attribution(self, attribution_id: UUID) -> Sequence[Evidence]:
        stmt = (
            select(EvidenceModel)
            .where(
                EvidenceModel.attribution_id == attribution_id,
                EvidenceModel.deleted_at.is_(None),
            )
            .order_by(EvidenceModel.created_at.desc())
        )
        return [
            EvidenceMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_by_attribution(self, attribution_id: UUID) -> int:
        stmt = select(func.count()).select_from(EvidenceModel).where(
            EvidenceModel.attribution_id == attribution_id,
            EvidenceModel.deleted_at.is_(None),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def delete_by_attribution(self, attribution_id: UUID) -> int:
        now = utcnow()
        stmt = select(EvidenceModel).where(
            EvidenceModel.attribution_id == attribution_id,
            EvidenceModel.deleted_at.is_(None),
        )
        models = list(self._session.execute(stmt).scalars())
        for model in models:
            model.deleted_at = now
        self._session.flush()
        return len(models)
```

### backend/app/infrastructure/persistence/repositories/notification_repository.py

```python
"""SQLAlchemy implementation of the Notification repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.notification import Notification
from app.domain.enums import NotificationStatus
from app.domain.repositories.notification_repository import (
    NotificationRepositoryContract,
)
from app.domain.repositories.specifications import NotificationFilter, PageRequest
from app.infrastructure.persistence.mappers import NotificationMapper
from app.infrastructure.persistence.models.notification import NotificationModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyNotificationRepository(NotificationRepositoryContract):
    """SQLAlchemy implementation of the Notification repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> Notification | None:
        model = self._session.get(NotificationModel, entity_id)
        return NotificationMapper.to_entity(model) if model else None

    def add(self, entity: Notification) -> Notification:
        model = NotificationMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return NotificationMapper.to_entity(model)

    def update(self, entity: Notification) -> Notification:
        model = self._session.get(NotificationModel, entity.id)
        if model is None:
            raise NotFoundError(f"Notification {entity.id} not found")
        NotificationMapper.to_model(entity, model)
        self._session.flush()
        return NotificationMapper.to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(NotificationModel, entity_id)
        if model is None:
            raise NotFoundError(f"Notification {entity_id} not found")
        self._session.delete(model)
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(NotificationModel).where(
            NotificationModel.id == entity_id
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_recipient(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        stmt = select(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id
        )
        stmt = apply_pagination(stmt, page, NotificationModel.created_at)
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def list_unread(
        self, recipient_id: UUID, page: PageRequest
    ) -> Sequence[Notification]:
        stmt = select(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id,
            NotificationModel.status.in_(
                [NotificationStatus.PENDING.value, NotificationStatus.SENT.value]
            ),
        )
        stmt = apply_pagination(stmt, page, NotificationModel.created_at)
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def count_unread(self, recipient_id: UUID) -> int:
        stmt = select(func.count()).select_from(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id,
            NotificationModel.status.in_(
                [NotificationStatus.PENDING.value, NotificationStatus.SENT.value]
            ),
        )
        return int(self._session.execute(stmt).scalar_one() or 0)

    def find(
        self, spec: NotificationFilter, page: PageRequest
    ) -> Sequence[Notification]:
        stmt = select(NotificationModel)
        if spec.recipient_id:
            stmt = stmt.where(NotificationModel.recipient_id == spec.recipient_id)
        if spec.organization_id:
            stmt = stmt.where(NotificationModel.organization_id == spec.organization_id)
        if spec.statuses:
            stmt = stmt.where(NotificationModel.status.in_(spec.statuses))
        if spec.channels:
            stmt = stmt.where(NotificationModel.channel.in_(spec.channels))
        if spec.event_types:
            stmt = stmt.where(NotificationModel.event_type.in_(spec.event_types))
        stmt = apply_pagination(stmt, page, NotificationModel.created_at)
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]

    def mark_all_read(self, recipient_id: UUID) -> int:
        now = utcnow()
        stmt = select(NotificationModel).where(
            NotificationModel.recipient_id == recipient_id,
            NotificationModel.status.in_(
                [NotificationStatus.PENDING.value, NotificationStatus.SENT.value]
            ),
        )
        models = list(self._session.execute(stmt).scalars())
        for model in models:
            model.status = NotificationStatus.READ.value
            model.read_at = now
        self._session.flush()
        return len(models)

    def list_pending_for_delivery(self, limit: int) -> Sequence[Notification]:
        if limit <= 0:
            return []
        stmt = (
            select(NotificationModel)
            .where(NotificationModel.status == NotificationStatus.PENDING.value)
            .order_by(NotificationModel.created_at.asc())
            .limit(limit)
        )
        return [
            NotificationMapper.to_entity(m)
            for m in self._session.execute(stmt).scalars()
        ]
```

### backend/app/infrastructure/persistence/repositories/audit_log_repository.py

```python
"""SQLAlchemy implementation of the AuditLog repository."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.audit_log_repository import AuditLogRepositoryContract
from app.domain.repositories.specifications import AuditLogFilter, PageRequest
from app.infrastructure.persistence.mappers import AuditLogMapper
from app.infrastructure.persistence.models.audit_log import AuditLogModel
from app.infrastructure.persistence.repositories._base import apply_pagination


class SQLAlchemyAuditLogRepository(AuditLogRepositoryContract):
    """SQLAlchemy implementation of the AuditLog repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, entity_id: UUID) -> AuditLog | None:
        model = self._session.get(AuditLogModel, entity_id)
        return AuditLogMapper.to_entity(model) if model else None

    def add(self, entity: AuditLog) -> AuditLog:
        model = AuditLogMapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return AuditLogMapper.to_entity(model)

    def update(self, entity: AuditLog) -> AuditLog:
        raise NotFoundError("Audit logs are immutable and cannot be updated")

    def delete(self, entity_id: UUID) -> None:
        raise NotFoundError("Audit logs are immutable and cannot be deleted")

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(AuditLogModel).where(
            AuditLogModel.id == entity_id
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def list_by_organization(
        self, organization_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLogModel).where(
            AuditLogModel.organization_id == organization_id
        )
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_resource(
        self, resource_type: str, resource_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLogModel).where(
            AuditLogModel.resource_type == resource_type,
            AuditLogModel.resource_id == resource_id,
        )
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_actor(
        self, actor_id: UUID, page: PageRequest
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLogModel).where(AuditLogModel.actor_id == actor_id)
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def _apply_filter(self, stmt: Select, spec: AuditLogFilter) -> Select:
        if spec.organization_id:
            stmt = stmt.where(AuditLogModel.organization_id == spec.organization_id)
        if spec.actor_id:
            stmt = stmt.where(AuditLogModel.actor_id == spec.actor_id)
        if spec.resource_type:
            stmt = stmt.where(AuditLogModel.resource_type == spec.resource_type)
        if spec.resource_id:
            stmt = stmt.where(AuditLogModel.resource_id == spec.resource_id)
        if spec.actions:
            stmt = stmt.where(AuditLogModel.action.in_(spec.actions))
        if spec.occurred_after:
            stmt = stmt.where(AuditLogModel.created_at >= spec.occurred_after)
        if spec.occurred_before:
            stmt = stmt.where(AuditLogModel.created_at <= spec.occurred_before)
        return stmt

    def find(self, spec: AuditLogFilter, page: PageRequest) -> Sequence[AuditLog]:
        stmt = self._apply_filter(select(AuditLogModel), spec)
        stmt = apply_pagination(stmt, page, AuditLogModel.created_at)
        return [AuditLogMapper.to_entity(m) for m in self._session.execute(stmt).scalars()]

    def count(self, spec: AuditLogFilter) -> int:
        stmt = self._apply_filter(select(func.count()).select_from(AuditLogModel), spec)
        return int(self._session.execute(stmt).scalar_one() or 0)
```

### backend/app/infrastructure/persistence/unit_of_work.py

```python
"""SQLAlchemy Unit of Work implementation."""

from __future__ import annotations

from types import TracebackType
from typing import Type

from sqlalchemy.orm import Session

from app.domain.repositories.base import UnitOfWork
from app.infrastructure.persistence.database import SessionFactory
from app.infrastructure.persistence.repositories import (
    SQLAlchemyAttributionRepository,
    SQLAlchemyAuditLogRepository,
    SQLAlchemyBusinessOutcomeRepository,
    SQLAlchemyEvidenceRepository,
    SQLAlchemyKPIRepository,
    SQLAlchemyKeyResultRepository,
    SQLAlchemyMetricSnapshotRepository,
    SQLAlchemyNotificationRepository,
    SQLAlchemyObjectiveRepository,
    SQLAlchemyOrganizationRepository,
    SQLAlchemyProjectRepository,
    SQLAlchemySprintRepository,
    SQLAlchemyTeamMembershipRepository,
    SQLAlchemyTeamRepository,
    SQLAlchemyUserRepository,
    SQLAlchemyWorkItemRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    """Transactional unit of work exposing all repositories."""

    def __init__(self) -> None:
        self._session: Session | None = None
        self.organizations: SQLAlchemyOrganizationRepository
        self.teams: SQLAlchemyTeamRepository
        self.users: SQLAlchemyUserRepository
        self.team_memberships: SQLAlchemyTeamMembershipRepository
        self.projects: SQLAlchemyProjectRepository
        self.sprints: SQLAlchemySprintRepository
        self.work_items: SQLAlchemyWorkItemRepository
        self.outcomes: SQLAlchemyBusinessOutcomeRepository
        self.kpis: SQLAlchemyKPIRepository
        self.metric_snapshots: SQLAlchemyMetricSnapshotRepository
        self.objectives: SQLAlchemyObjectiveRepository
        self.key_results: SQLAlchemyKeyResultRepository
        self.attributions: SQLAlchemyAttributionRepository
        self.evidence: SQLAlchemyEvidenceRepository
        self.notifications: SQLAlchemyNotificationRepository
        self.audit_logs: SQLAlchemyAuditLogRepository

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("UnitOfWork is not active; use it as a context manager")
        return self._session

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        self._session = SessionFactory()
        self._build_repositories(self._session)
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc is not None:
                self.rollback()
        finally:
            if self._session is not None:
                self._session.close()
            self._session = None

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def _build_repositories(self, session: Session) -> None:
        self.organizations = SQLAlchemyOrganizationRepository(session)
        self.teams = SQLAlchemyTeamRepository(session)
        self.users = SQLAlchemyUserRepository(session)
        self.team_memberships = SQLAlchemyTeamMembershipRepository(session)
        self.projects = SQLAlchemyProjectRepository(session)
        self.sprints = SQLAlchemySprintRepository(session)
        self.work_items = SQLAlchemyWorkItemRepository(session)
        self.outcomes = SQLAlchemyBusinessOutcomeRepository(session)
        self.kpis = SQLAlchemyKPIRepository(session)
        self.metric_snapshots = SQLAlchemyMetricSnapshotRepository(session)
        self.objectives = SQLAlchemyObjectiveRepository(session)
        self.key_results = SQLAlchemyKeyResultRepository(session)
        self.attributions = SQLAlchemyAttributionRepository(session)
        self.evidence = SQLAlchemyEvidenceRepository(session)
        self.notifications = SQLAlchemyNotificationRepository(session)
        self.audit_logs = SQLAlchemyAuditLogRepository(session)
```

### backend/app/application/__init__.py

```python
"""Application layer - use cases, commands, queries, DTOs."""
```

### backend/app/application/dtos/__init__.py

```python
"""Data Transfer Objects used by the application layer."""

from app.application.dtos.attribution import (
    AttributionCreateDTO,
    AttributionDTO,
    AttributionUpdateDTO,
    EvidenceCreateDTO,
    EvidenceDTO,
)
from app.application.dtos.auth import LoginDTO, RefreshTokenDTO, TokenDTO
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.kpi import (
    KPICreateDTO,
    KPIDTO,
    KPIUpdateDTO,
    MetricSnapshotCreateDTO,
    MetricSnapshotDTO,
)
from app.application.dtos.notification import NotificationCreateDTO, NotificationDTO
from app.application.dtos.okr import (
    KeyResultCreateDTO,
    KeyResultDTO,
    KeyResultUpdateDTO,
    ObjectiveCreateDTO,
    ObjectiveDTO,
    ObjectiveUpdateDTO,
)
from app.application.dtos.organization import (
    OrganizationCreateDTO,
    OrganizationDTO,
    OrganizationUpdateDTO,
    TeamCreateDTO,
    TeamDTO,
    TeamUpdateDTO,
)
from app.application.dtos.outcome import (
    BusinessOutcomeCreateDTO,
    BusinessOutcomeDTO,
    BusinessOutcomeUpdateDTO,
)
from app.application.dtos.project import ProjectCreateDTO, ProjectDTO, ProjectUpdateDTO
from app.application.dtos.sprint import (
    SprintCompleteDTO,
    SprintCreateDTO,
    SprintDTO,
    SprintUpdateDTO,
)
from app.application.dtos.user import (
    UserCreateDTO,
    UserDTO,
    UserInviteDTO,
    UserUpdateDTO,
)
from app.application.dtos.work_item import (
    WorkItemCreateDTO,
    WorkItemDTO,
    WorkItemUpdateDTO,
)

__all__ = [
    "AttributionCreateDTO",
    "AttributionDTO",
    "AttributionUpdateDTO",
    "BusinessOutcomeCreateDTO",
    "BusinessOutcomeDTO",
    "BusinessOutcomeUpdateDTO",
    "EvidenceCreateDTO",
    "EvidenceDTO",
    "KPICreateDTO",
    "KPIDTO",
    "KPIUpdateDTO",
    "KeyResultCreateDTO",
    "KeyResultDTO",
    "KeyResultUpdateDTO",
    "LoginDTO",
    "MetricSnapshotCreateDTO",
    "MetricSnapshotDTO",
    "NotificationCreateDTO",
    "NotificationDTO",
    "ObjectiveCreateDTO",
    "ObjectiveDTO",
    "ObjectiveUpdateDTO",
    "OrganizationCreateDTO",
    "OrganizationDTO",
    "OrganizationUpdateDTO",
    "PageDTO",
    "PaginatedResultDTO",
    "ProjectCreateDTO",
    "ProjectDTO",
    "ProjectUpdateDTO",
    "RefreshTokenDTO",
    "SprintCompleteDTO",
    "SprintCreateDTO",
    "SprintDTO",
    "SprintUpdateDTO",
    "TeamCreateDTO",
    "TeamDTO",
    "TeamUpdateDTO",
    "TokenDTO",
    "UserCreateDTO",
    "UserDTO",
    "UserInviteDTO",
    "UserUpdateDTO",
    "WorkItemCreateDTO",
    "WorkItemDTO",
    "WorkItemUpdateDTO",
]
```

### backend/app/application/dtos/common.py

```python
"""Common DTOs used across the application layer."""

from __future__ import annotations

from typing import Generic, List, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PageDTO(BaseModel):
    """Pagination request DTO."""

    model_config = ConfigDict(frozen=True)

    limit: int = Field(default=20, ge=1, le=500)
    offset: int = Field(default=0, ge=0)
    order_by: str = Field(default="created_at")
    descending: bool = Field(default=True)


class PaginatedResultDTO(BaseModel, Generic[T]):
    """Paginated result envelope."""

    items: List[T]
    total: int
    limit: int
    offset: int

    @property
    def has_more(self) -> bool:
        return (self.offset + len(self.items)) < self.total
```

### backend/app/application/dtos/auth.py

```python
"""Authentication DTOs."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class LoginDTO(BaseModel):
    """Login credentials."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenDTO(BaseModel):
    """Access + refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenDTO(BaseModel):
    """Refresh token request."""

    refresh_token: str = Field(min_length=1)
```

### backend/app/application/dtos/organization.py

```python
"""Organization and Team DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OrganizationCreateDTO(BaseModel):
    """Payload for creating an organization."""

    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=2, max_length=64)
    description: str | None = Field(default=None, max_length=2000)
    billing_email: EmailStr | None = None


class OrganizationUpdateDTO(BaseModel):
    """Payload for updating an organization."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    billing_email: EmailStr | None = None
    is_active: bool | None = None


class OrganizationDTO(BaseModel):
    """Organization response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: str | None
    billing_email: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TeamCreateDTO(BaseModel):
    """Payload for creating a team."""

    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=2, max_length=64)
    description: str | None = Field(default=None, max_length=2000)


class TeamUpdateDTO(BaseModel):
    """Payload for updating a team."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class TeamDTO(BaseModel):
    """Team response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    slug: str
    description: str | None
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/user.py

```python
"""User DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.enums import UserRole, UserStatus


class UserCreateDTO(BaseModel):
    """Payload for creating a user (self-registration or admin create)."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)
    organization_id: UUID | None = None
    role: UserRole = UserRole.VIEWER


class UserInviteDTO(BaseModel):
    """Payload for inviting a user to an organization."""

    email: EmailStr
    full_name: str = Field(min_length=1, max_length=200)
    role: UserRole = UserRole.VIEWER


class UserUpdateDTO(BaseModel):
    """Payload for updating a user."""

    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    role: UserRole | None = None
    status: UserStatus | None = None


class UserDTO(BaseModel):
    """User response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: str
    organization_id: UUID | None
    role: UserRole
    status: UserStatus
    last_login_at: datetime | None
    is_email_verified: bool
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/project.py

```python
"""Project DTOs."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectCreateDTO(BaseModel):
    """Payload for creating a project."""

    team_id: UUID
    name: str = Field(min_length=1, max_length=200)
    key: str = Field(min_length=2, max_length=12)
    slug: str = Field(min_length=2, max_length=64)
    description: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None
    target_end_date: date | None = None

    @field_validator("key")
    @classmethod
    def _uppercase_key(cls, v: str) -> str:
        return v.upper()


class ProjectUpdateDTO(BaseModel):
    """Payload for updating a project."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None
    target_end_date: date | None = None
    is_archived: bool | None = None


class ProjectDTO(BaseModel):
    """Project response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    team_id: UUID
    name: str
    key: str
    slug: str
    description: str | None
    start_date: date | None
    target_end_date: date | None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/sprint.py

```python
"""Sprint DTOs."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import SprintStatus


class SprintCreateDTO(BaseModel):
    """Payload for creating a sprint."""

    project_id: UUID
    name: str = Field(min_length=1, max_length=200)
    goal: str | None = Field(default=None, max_length=2000)
    start_date: date
    end_date: date
    planned_capacity: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def _validate_dates(self) -> "SprintCreateDTO":
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class SprintUpdateDTO(BaseModel):
    """Payload for updating a sprint."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    goal: str | None = Field(default=None, max_length=2000)
    start_date: date | None = None
    end_date: date | None = None
    planned_capacity: int | None = Field(default=None, ge=0)


class SprintCompleteDTO(BaseModel):
    """Payload for completing a sprint."""

    completed_points: int = Field(ge=0)


class SprintDTO(BaseModel):
    """Sprint response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    goal: str | None
    start_date: date
    end_date: date
    status: SprintStatus
    started_at: datetime | None
    completed_at: datetime | None
    planned_capacity: int
    completed_points: int
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/work_item.py

```python
"""Work item DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType


class WorkItemCreateDTO(BaseModel):
    """Payload for creating a work item."""

    project_id: UUID
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    external_key: str | None = Field(default=None, max_length=64)
    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    item_type: WorkItemType = WorkItemType.STORY
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    story_points: int | None = Field(default=None, ge=0, le=1000)
    estimated_hours: float | None = Field(default=None, ge=0)
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    labels: list[str] = Field(default_factory=list)


class WorkItemUpdateDTO(BaseModel):
    """Payload for updating a work item."""

    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    priority: WorkItemPriority | None = None
    status: WorkItemStatus | None = None
    story_points: int | None = Field(default=None, ge=0, le=1000)
    estimated_hours: float | None = Field(default=None, ge=0)
    actual_hours: float | None = Field(default=None, ge=0)
    assignee_id: UUID | None = None
    labels: list[str] | None = None


class WorkItemDTO(BaseModel):
    """Work item response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    sprint_id: UUID | None
    parent_id: UUID | None
    epic_id: UUID | None
    external_key: str | None
    title: str
    description: str | None
    item_type: WorkItemType
    status: WorkItemStatus
    priority: WorkItemPriority
    story_points: int | None
    estimated_hours: float | None
    actual_hours: float | None
    assignee_id: UUID | None
    reporter_id: UUID | None
    labels: list[str]
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/outcome.py

```python
"""Business outcome DTOs."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import OutcomeStatus


class BusinessOutcomeCreateDTO(BaseModel):
    """Payload for creating a business outcome."""

    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    hypothesis: str | None = Field(default=None, max_length=4000)
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = Field(default=None, ge=0, le=100)
    financial_impact_estimate: Decimal | None = None


class BusinessOutcomeUpdateDTO(BaseModel):
    """Payload for updating a business outcome."""

    owner_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    hypothesis: str | None = Field(default=None, max_length=4000)
    status: OutcomeStatus | None = None
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = Field(default=None, ge=0, le=100)
    financial_impact_estimate: Decimal | None = None


class BusinessOutcomeDTO(BaseModel):
    """Business outcome response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    owner_id: UUID | None
    name: str
    description: str | None
    hypothesis: str | None
    status: OutcomeStatus
    target_date: date | None
    baseline_value: Decimal | None
    target_value: Decimal | None
    current_value: Decimal | None
    progress_percent: Decimal
    confidence_score: Decimal | None
    financial_impact_estimate: Decimal | None
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/kpi.py

```python
"""KPI and metric snapshot DTOs."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import KPIDirection, KPIUnit


class KPICreateDTO(BaseModel):
    """Payload for creating a KPI."""

    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    unit: KPIUnit = KPIUnit.COUNT
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    direction: KPIDirection = KPIDirection.INCREASE
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = Field(default=None, max_length=500)
    refresh_frequency_hours: int | None = Field(default=None, ge=1, le=8760)


class KPIUpdateDTO(BaseModel):
    """Payload for updating a KPI."""

    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    direction: KPIDirection | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = Field(default=None, max_length=500)
    refresh_frequency_hours: int | None = Field(default=None, ge=1, le=8760)
    is_active: bool | None = None


class KPIDTO(BaseModel):
    """KPI response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    outcome_id: UUID | None
    owner_id: UUID | None
    name: str
    description: str | None
    unit: KPIUnit
    currency: str | None
    direction: KPIDirection
    baseline_value: Decimal | None
    target_value: Decimal | None
    current_value: Decimal | None
    data_source: str | None
    refresh_frequency_hours: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MetricSnapshotCreateDTO(BaseModel):
    """Payload for recording a KPI metric snapshot."""

    kpi_id: UUID
    value: Decimal
    recorded_at: datetime | None = None
    source: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)
    context: dict[str, str] = Field(default_factory=dict)


class MetricSnapshotDTO(BaseModel):
    """Metric snapshot response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    kpi_id: UUID
    value: Decimal
    recorded_at: datetime
    source: str | None
    notes: str | None
    context: dict[str, str]
    created_at: datetime
```

### backend/app/application/dtos/okr.py

```python
"""OKR DTOs."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import OKRStatus, OKRType


class ObjectiveCreateDTO(BaseModel):
    """Payload for creating an objective."""

    team_id: UUID | None = None
    owner_id: UUID | None = None
    parent_id: UUID | None = None
    title: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    okr_type: OKRType = OKRType.TEAM
    period_start: date
    period_end: date

    @model_validator(mode="after")
    def _validate_period(self) -> "ObjectiveCreateDTO":
        if self.period_end < self.period_start:
            raise ValueError("period_end cannot be before period_start")
        if self.okr_type == OKRType.TEAM and self.team_id is None:
            raise ValueError("team_id is required for team-level objectives")
        return self


class ObjectiveUpdateDTO(BaseModel):
    """Payload for updating an objective."""

    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    owner_id: UUID | None = None
    status: OKRStatus | None = None
    period_start: date | None = None
    period_end: date | None = None


class ObjectiveDTO(BaseModel):
    """Objective response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    team_id: UUID | None
    owner_id: UUID | None
    parent_id: UUID | None
    title: str
    description: str | None
    okr_type: OKRType
    status: OKRStatus
    period_start: date
    period_end: date
    created_at: datetime
    updated_at: datetime


class KeyResultCreateDTO(BaseModel):
    """Payload for creating a key result."""

    objective_id: UUID
    kpi_id: UUID | None = None
    title: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    baseline_value: Decimal
    target_value: Decimal
    current_value: Decimal = Decimal("0")
    weight: Decimal = Field(default=Decimal("1"), gt=0)


class KeyResultUpdateDTO(BaseModel):
    """Payload for updating a key result."""

    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    weight: Decimal | None = Field(default=None, gt=0)
    status: OKRStatus | None = None


class KeyResultDTO(BaseModel):
    """Key result response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    objective_id: UUID
    kpi_id: UUID | None
    title: str
    description: str | None
    baseline_value: Decimal
    target_value: Decimal
    current_value: Decimal
    progress_percent: Decimal
    weight: Decimal
    status: OKRStatus
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/attribution.py

```python
"""Attribution and evidence DTOs."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.enums import AttributionMethod, AttributionStrength


class AttributionCreateDTO(BaseModel):
    """Payload for creating an outcome attribution."""

    work_item_id: UUID | None = None
    sprint_id: UUID | None = None
    outcome_id: UUID | None = None
    kpi_id: UUID | None = None
    key_result_id: UUID | None = None
    method: AttributionMethod = AttributionMethod.MANUAL
    strength: AttributionStrength = AttributionStrength.CONTRIBUTING
    weight: Decimal = Field(default=Decimal("1"), gt=0)
    confidence: Decimal = Field(default=Decimal("50"), ge=0, le=100)
    estimated_value: Decimal | None = None
    rationale: str | None = Field(default=None, max_length=4000)

    @model_validator(mode="after")
    def _validate_relations(self) -> "AttributionCreateDTO":
        if self.work_item_id is None and self.sprint_id is None:
            raise ValueError("At least one of work_item_id or sprint_id is required")
        if self.outcome_id is None and self.kpi_id is None and self.key_result_id is None:
            raise ValueError(
                "At least one of outcome_id, kpi_id, or key_result_id is required"
            )
        return self


class AttributionUpdateDTO(BaseModel):
    """Payload for updating an attribution."""

    strength: AttributionStrength | None = None
    weight: Decimal | None = Field(default=None, gt=0)
    confidence: Decimal | None = Field(default=None, ge=0, le=100)
    estimated_value: Decimal | None = None
    rationale: str | None = Field(default=None, max_length=4000)


class AttributionDTO(BaseModel):
    """Attribution response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    work_item_id: UUID | None
    sprint_id: UUID | None
    outcome_id: UUID | None
    kpi_id: UUID | None
    key_result_id: UUID | None
    attributed_by_id: UUID | None
    method: AttributionMethod
    strength: AttributionStrength
    weight: Decimal
    confidence: Decimal
    estimated_value: Decimal | None
    rationale: str | None
    created_at: datetime
    updated_at: datetime


class EvidenceCreateDTO(BaseModel):
    """Payload for creating evidence."""

    attribution_id: UUID
    title: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1, max_length=10000)
    source_url: str | None = Field(default=None, max_length=2000)
    evidence_type: str = Field(default="note", max_length=32)


class EvidenceDTO(BaseModel):
    """Evidence response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    attribution_id: UUID
    author_id: UUID | None
    title: str
    content: str
    source_url: str | None
    evidence_type: str
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/dtos/notification.py

```python
"""Notification DTOs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import NotificationChannel, NotificationStatus


class NotificationCreateDTO(BaseModel):
    """Payload for creating a notification."""

    recipient_id: UUID
    title: str = Field(min_length=1, max_length=300)
    body: str = Field(min_length=1, max_length=4000)
    channel: NotificationChannel = NotificationChannel.IN_APP
    event_type: str = Field(default="generic", max_length=64)
    subject_type: str | None = Field(default=None, max_length=64)
    subject_id: UUID | None = None
    action_url: str | None = Field(default=None, max_length=2000)


class NotificationDTO(BaseModel):
    """Notification response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    recipient_id: UUID
    organization_id: UUID
    title: str
    body: str
    channel: NotificationChannel
    status: NotificationStatus
    event_type: str
    subject_type: str | None
    subject_id: UUID | None
    action_url: str | None
    sent_at: datetime | None
    read_at: datetime | None
    created_at: datetime
```

### backend/app/application/mappers.py

```python
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
```

### backend/app/application/context.py

```python
"""Execution context passed to use cases."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.user import User


@dataclass(frozen=True)
class RequestContext:
    """Context capturing the acting user and request metadata."""

    actor: User
    ip_address: str | None = None
    user_agent: str | None = None

    @property
    def actor_id(self) -> UUID:
        return self.actor.id

    @property
    def organization_id(self) -> UUID | None:
        return self.actor.organization_id
```

### backend/app/application/use_cases/base.py

```python
"""Base classes for application use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class UseCase(ABC, Generic[TCommand, TResult]):
    """Base use case protocol."""

    def __init__(self, uow_factory: type[SQLAlchemyUnitOfWork] = SQLAlchemyUnitOfWork) -> None:
        self._uow_factory = uow_factory

    @abstractmethod
    def execute(self, command: TCommand) -> TResult:
        """Execute the use case."""
```

### backend/app/application/use_cases/auth/__init__.py

```python
"""Authentication use cases."""

from app.application.use_cases.auth.login import LoginCommand, LoginUseCase
from app.application.use_cases.auth.refresh_token import (
    RefreshTokenCommand,
    RefreshTokenUseCase,
)
from app.application.use_cases.auth.register import RegisterCommand, RegisterUseCase

__all__ = [
    "LoginCommand",
    "LoginUseCase",
    "RefreshTokenCommand",
    "RefreshTokenUseCase",
    "RegisterCommand",
    "RegisterUseCase",
]
```

### backend/app/application/use_cases/auth/login.py

```python
"""Login use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.application.dtos.auth import TokenDTO
from app.application.use_cases.base import UseCase
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.domain.enums import UserStatus


@dataclass(frozen=True)
class LoginCommand:
    """Login command payload."""

    email: str
    password: str
    ip_address: str | None = None
    user_agent: str | None = None


class LoginUseCase(UseCase[LoginCommand, TokenDTO]):
    """Authenticate a user and return an access/refresh token pair."""

    def execute(self, command: LoginCommand) -> TokenDTO:
        with self._uow_factory() as uow:
            user = uow.users.get_by_email(command.email)
            if user is None:
                raise AuthenticationError("Invalid email or password")
            if not verify_password(command.password, user.hashed_password):
                raise AuthenticationError("Invalid email or password")
            if user.status != UserStatus.ACTIVE:
                raise AuthenticationError(
                    f"Account is not active (status: {user.status.value})"
                )

            user.record_login(datetime.now(timezone.utc))
            uow.users.update(user)
            uow.commit()

            access_token = create_access_token(
                subject=user.id,
                additional_claims={
                    "role": user.role.value,
                    "org": str(user.organization_id) if user.organization_id else None,
                },
            )
            refresh_token = create_refresh_token(subject=user.id)

            return TokenDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
```

### backend/app/application/use_cases/auth/refresh_token.py

```python
"""Refresh access token use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.auth import TokenDTO
from app.application.use_cases.base import UseCase
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.domain.enums import UserStatus


@dataclass(frozen=True)
class RefreshTokenCommand:
    """Refresh token command payload."""

    refresh_token: str


class RefreshTokenUseCase(UseCase[RefreshTokenCommand, TokenDTO]):
    """Issue a new access token given a valid refresh token."""

    def execute(self, command: RefreshTokenCommand) -> TokenDTO:
        payload = decode_token(command.refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Provided token is not a refresh token")

        subject = payload.get("sub")
        if not subject:
            raise AuthenticationError("Refresh token missing subject")

        try:
            user_id = UUID(subject)
        except ValueError as exc:
            raise AuthenticationError("Invalid subject in token") from exc

        with self._uow_factory() as uow:
            user = uow.users.get_by_id(user_id)
            if user is None or user.status != UserStatus.ACTIVE:
                raise AuthenticationError("User is not active")

            access_token = create_access_token(
                subject=user.id,
                additional_claims={
                    "role": user.role.value,
                    "org": str(user.organization_id) if user.organization_id else None,
                },
            )
            refresh_token = create_refresh_token(subject=user.id)

            return TokenDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
```

### backend/app/application/use_cases/auth/register.py

```python
"""User self-registration use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.user import UserDTO
from app.application.mappers import user_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import ConflictError
from app.core.security import hash_password
from app.domain.entities.user import User
from app.domain.enums import UserRole, UserStatus
from app.domain.value_objects import Email


@dataclass(frozen=True)
class RegisterCommand:
    """Register command payload."""

    email: str
    password: str
    full_name: str
    organization_id: UUID | None = None
    role: UserRole = UserRole.VIEWER


class RegisterUseCase(UseCase[RegisterCommand, UserDTO]):
    """Register a new user account."""

    def execute(self, command: RegisterCommand) -> UserDTO:
        with self._uow_factory() as uow:
            if uow.users.email_exists(command.email):
                raise ConflictError(f"Email {command.email} is already registered")

            user = User(
                email=Email(command.email),
                hashed_password=hash_password(command.password),
                full_name=command.full_name,
                organization_id=command.organization_id,
                role=command.role,
                status=UserStatus.ACTIVE,
                is_email_verified=False,
            )
            created = uow.users.add(user)
            uow.commit()
            return user_to_dto(created)
```

### backend/app/application/use_cases/organizations/__init__.py

```python
"""Organization use cases."""

from app.application.use_cases.organizations.create_organization import (
    CreateOrganizationCommand,
    CreateOrganizationUseCase,
)
from app.application.use_cases.organizations.get_organization import (
    GetOrganizationQuery,
    GetOrganizationUseCase,
)
from app.application.use_cases.organizations.list_organizations import (
    ListOrganizationsQuery,
    ListOrganizationsUseCase,
)
from app.application.use_cases.organizations.update_organization import (
    UpdateOrganizationCommand,
    UpdateOrganizationUseCase,
)

__all__ = [
    "CreateOrganizationCommand",
    "CreateOrganizationUseCase",
    "GetOrganizationQuery",
    "GetOrganizationUseCase",
    "ListOrganizationsQuery",
    "ListOrganizationsUseCase",
    "UpdateOrganizationCommand",
    "UpdateOrganizationUseCase",
]
```

### backend/app/application/use_cases/organizations/create_organization.py

```python
"""Create organization use case."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.context import RequestContext
from app.application.dtos.organization import OrganizationDTO
from app.application.mappers import organization_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import ConflictError
from app.domain.entities.organization import Organization
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug


@dataclass(frozen=True)
class CreateOrganizationCommand:
    """Create organization command."""

    name: str
    slug: str
    description: str | None
    billing_email: str | None
    context: RequestContext


class CreateOrganizationUseCase(UseCase[CreateOrganizationCommand, OrganizationDTO]):
    """Create a new organization."""

    def execute(self, command: CreateOrganizationCommand) -> OrganizationDTO:
        AuthorizationDomainService.ensure(
            AuthorizationDomainService.can_manage_organization(command.context.actor),
            "Only administrators can create organizations",
        )

        with self._uow_factory() as uow:
            if uow.organizations.slug_exists(command.slug):
                raise ConflictError(f"Organization slug '{command.slug}' is already in use")

            organization = Organization(
                name=command.name,
                slug=Slug(command.slug),
                description=command.description,
                billing_email=command.billing_email,
                is_active=True,
            )
            created = uow.organizations.add(organization)
            uow.commit()
            return organization_to_dto(created)
```

### backend/app/application/use_cases/organizations/get_organization.py

```python
"""Get organization use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.organization import OrganizationDTO
from app.application.mappers import organization_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService


@dataclass(frozen=True)
class GetOrganizationQuery:
    """Query for retrieving an organization."""

    organization_id: UUID
    context: RequestContext


class GetOrganizationUseCase(UseCase[GetOrganizationQuery, OrganizationDTO]):
    """Retrieve an organization by ID."""

    def execute(self, query: GetOrganizationQuery) -> OrganizationDTO:
        AuthorizationDomainService.ensure_same_organization(
            query.context.actor, query.organization_id
        )

        with self._uow_factory() as uow:
            organization = uow.organizations.get_by_id(query.organization_id)
            if organization is None:
                raise NotFoundError(f"Organization {query.organization_id} not found")
            return organization_to_dto(organization)
```

### backend/app/application/use_cases/organizations/list_organizations.py

```python
"""List organizations use case."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.organization import OrganizationDTO
from app.application.mappers import organization_to_dto
from app.application.use_cases.base import UseCase
from app.domain.enums import UserRole
from app.domain.repositories.specifications import PageRequest


@dataclass(frozen=True)
class ListOrganizationsQuery:
    """Query for listing organizations."""

    page: PageDTO
    context: RequestContext


class ListOrganizationsUseCase(
    UseCase[ListOrganizationsQuery, PaginatedResultDTO[OrganizationDTO]]
):
    """List organizations visible to the actor."""

    def execute(
        self, query: ListOrganizationsQuery
    ) -> PaginatedResultDTO[OrganizationDTO]:
        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )

        with self._uow_factory() as uow:
            if query.context.actor.role == UserRole.SUPER_ADMIN:
                items = uow.organizations.list_all(page)
                total = uow.organizations.count()
            elif query.context.actor.organization_id is not None:
                org = uow.organizations.get_by_id(query.context.actor.organization_id)
                items = [org] if org is not None else []
                total = 1 if org is not None else 0
            else:
                items = []
                total = 0

            return PaginatedResultDTO[OrganizationDTO](
                items=[organization_to_dto(o) for o in items],
                total=total,
                limit=page.limit,
                offset=page.offset,
            )
```

### backend/app/application/use_cases/organizations/update_organization.py

```python
"""Update organization use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.organization import OrganizationDTO
from app.application.mappers import organization_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService


@dataclass(frozen=True)
class UpdateOrganizationCommand:
    """Update organization command."""

    organization_id: UUID
    name: str | None
    description: str | None
    billing_email: str | None
    is_active: bool | None
    context: RequestContext


class UpdateOrganizationUseCase(UseCase[UpdateOrganizationCommand, OrganizationDTO]):
    """Update an existing organization."""

    def execute(self, command: UpdateOrganizationCommand) -> OrganizationDTO:
        AuthorizationDomainService.ensure(
            AuthorizationDomainService.can_manage_organization(command.context.actor),
            "Only administrators can update organizations",
        )
        AuthorizationDomainService.ensure_same_organization(
            command.context.actor, command.organization_id
        )

        with self._uow_factory() as uow:
            org = uow.organizations.get_by_id(command.organization_id)
            if org is None:
                raise NotFoundError(f"Organization {command.organization_id} not found")

            if command.name is not None:
                org.rename(command.name)
            if command.description is not None:
                org.description = command.description
                org.touch()
            if command.billing_email is not None:
                org.billing_email = command.billing_email
                org.touch()
            if command.is_active is not None:
                if command.is_active:
                    org.activate()
                else:
                    org.deactivate()

            updated = uow.organizations.update(org)
            uow.commit()
            return organization_to_dto(updated)
```

### backend/app/application/services/__init__.py

```python
"""Application services - stateful coordinators reused by use cases."""

from app.application.services.audit_service import AuditService
from app.application.services.notification_service import NotificationService

__all__ = ["AuditService", "NotificationService"]
```

### backend/app/application/services/audit_service.py

```python
"""Audit logging application service."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from app.domain.entities.audit_log import AuditLog
from app.domain.enums import AuditAction
from app.domain.repositories.audit_log_repository import AuditLogRepositoryContract


class AuditService:
    """Writes audit log entries via the provided repository."""

    def __init__(self, repository: AuditLogRepositoryContract) -> None:
        self._repository = repository

    def record(
        self,
        *,
        organization_id: UUID,
        actor_id: UUID | None,
        action: AuditAction,
        resource_type: str,
        resource_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        changes: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        """Persist an audit entry."""
        entry = AuditLog(
            organization_id=organization_id,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            changes=changes or {},
            metadata=metadata or {},
        )
        return self._repository.add(entry)
```

### backend/app/application/services/notification_service.py

```python
"""Notification application service."""

from __future__ import annotations

from uuid import UUID

from app.domain.entities.notification import Notification
from app.domain.enums import NotificationChannel, NotificationStatus
from app.domain.repositories.notification_repository import (
    NotificationRepositoryContract,
)


class NotificationService:
    """Creates and dispatches user-facing notifications."""

    def __init__(self, repository: NotificationRepositoryContract) -> None:
        self._repository = repository

    def notify(
        self,
        *,
        recipient_id: UUID,
        organization_id: UUID,
        title: str,
        body: str,
        event_type: str,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        subject_type: str | None = None,
        subject_id: UUID | None = None,
        action_url: str | None = None,
    ) -> Notification:
        """Create a pending notification for a recipient."""
        notification = Notification(
            recipient_id=recipient_id,
            organization_id=organization_id,
            title=title,
            body=body,
            channel=channel,
            status=NotificationStatus.PENDING,
            event_type=event_type,
            subject_type=subject_type,
            subject_id=subject_id,
            action_url=action_url,
        )
        return self._repository.add(notification)

    def mark_read(self, notification_id: UUID) -> Notification:
        """Mark a notification as read."""
        notification = self._repository.get_by_id(notification_id)
        if notification is None:
            raise ValueError(f"Notification {notification_id} not found")
        notification.mark_read()
        return self._repository.update(notification)

    def mark_all_read(self, recipient_id: UUID) -> int:
        """Mark all pending/sent notifications for a recipient as read."""
        return self._repository.mark_all_read(recipient_id)
```

================================================================================

### backend/app/application/use_cases/__init__.py

```python
"""Application use cases."""
```

### backend/app/api/__init__.py

```python
"""API layer - FastAPI routers, dependencies, schemas."""
```

### backend/app/api/schemas/__init__.py

```python
"""API request/response schemas."""

from app.api.schemas.common import ErrorResponse, HealthResponse, MessageResponse

__all__ = ["ErrorResponse", "HealthResponse", "MessageResponse"]
```

### backend/app/api/schemas/common.py

```python
"""Common API response schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response body."""

    error: str = Field(description="Machine-readable error code")
    message: str = Field(description="Human-readable message")
    details: dict[str, Any] = Field(default_factory=dict)


class MessageResponse(BaseModel):
    """Simple message envelope."""

    message: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    environment: str
```

### backend/app/api/exception_handlers.py

```python
"""Central exception handlers for the FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    ApplicationError,
    AuthenticationError,
    AuthorizationError,
    BusinessRuleViolationError,
    ConflictError,
    ExternalServiceError,
    NotFoundError,
    ValidationError,
)
from app.core.logging import get_logger

_logger = get_logger("api.exceptions")


def _payload(code: str, message: str, details: dict | None = None) -> dict:
    return {"error": code, "message": message, "details": details or {}}


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers on the FastAPI application."""

    @app.exception_handler(NotFoundError)
    async def _not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("not_found", exc.message, exc.details),
        )

    @app.exception_handler(ConflictError)
    async def _conflict(_: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("conflict", exc.message, exc.details),
        )

    @app.exception_handler(ValidationError)
    async def _validation(_: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("validation_error", exc.message, exc.details),
        )

    @app.exception_handler(BusinessRuleViolationError)
    async def _business(_: Request, exc: BusinessRuleViolationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("business_rule_violation", exc.message, exc.details),
        )

    @app.exception_handler(AuthenticationError)
    async def _auth(_: Request, exc: AuthenticationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("unauthenticated", exc.message, exc.details),
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(AuthorizationError)
    async def _authz(_: Request, exc: AuthorizationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("forbidden", exc.message, exc.details),
        )

    @app.exception_handler(ExternalServiceError)
    async def _external(_: Request, exc: ExternalServiceError) -> JSONResponse:
        _logger.error("External service error: %s", exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("external_service_error", exc.message, exc.details),
        )

    @app.exception_handler(ApplicationError)
    async def _application(_: Request, exc: ApplicationError) -> JSONResponse:
        _logger.exception("Unhandled application error")
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("application_error", exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def _request_validation(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_payload(
                "request_validation_error",
                "Request validation failed",
                {"errors": exc.errors()},
            ),
        )

    @app.exception_handler(IntegrityError)
    async def _integrity(_: Request, exc: IntegrityError) -> JSONResponse:
        _logger.warning("Database integrity error: %s", exc)
        return JSONResponse(
            status_code=409,
            content=_payload(
                "conflict",
                "The request could not be completed due to a data conflict.",
            ),
        )

    @app.exception_handler(SQLAlchemyError)
    async def _database(_: Request, exc: SQLAlchemyError) -> JSONResponse:
        _logger.exception("Database error")
        return JSONResponse(
            status_code=500,
            content=_payload("database_error", "A database error occurred."),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload("http_error", str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        _logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content=_payload("internal_error", "An unexpected error occurred."),
        )
```

### backend/app/api/dependencies.py

```python
"""FastAPI dependency providers."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer

from app.application.context import RequestContext
from app.application.services.audit_service import AuditService
from app.application.services.notification_service import NotificationService
from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token
from app.domain.entities.user import User
from app.domain.enums import UserRole
from app.domain.services.authorization_service import AuthorizationDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False,
)


def get_uow_factory() -> type[SQLAlchemyUnitOfWork]:
    """Return the concrete Unit-of-Work factory type."""
    return SQLAlchemyUnitOfWork


def get_uow() -> SQLAlchemyUnitOfWork:
    """Return an unopened Unit-of-Work instance. Callers must use it as a ctx manager."""
    return SQLAlchemyUnitOfWork()


def get_current_user(
    request: Request,
    token: Annotated[str | None, Depends(_oauth2_scheme)],
) -> User:
    """Resolve the current authenticated user from a Bearer token."""
    if not token:
        raise AuthenticationError("Authentication credentials were not provided")

    payload = decode_token(token)
    if payload.get("type") != "access":
        raise AuthenticationError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise AuthenticationError("Token missing subject")

    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise AuthenticationError("Invalid subject in token") from exc

    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise AuthenticationError("User not found")
        if not user.is_active:
            raise AuthenticationError("User account is not active")

    # Cache on request for downstream services
    request.state.current_user = user
    return user


def get_request_context(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    x_forwarded_for: Annotated[str | None, Header(alias="X-Forwarded-For")] = None,
) -> RequestContext:
    """Build a RequestContext for use cases."""
    ip_address = x_forwarded_for or (request.client.host if request.client else None)
    user_agent = request.headers.get("user-agent")
    return RequestContext(
        actor=current_user,
        ip_address=ip_address,
        user_agent=user_agent,
    )


def require_roles(*roles: UserRole):
    """Return a dependency that requires the current user to have one of the given roles."""

    def _dependency(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in roles:
            raise AuthorizationError(
                f"This action requires one of roles: {', '.join(r.value for r in roles)}"
            )
        return user

    return _dependency


def require_admin(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require an admin-level user."""
    if not AuthorizationDomainService.can_manage_organization(user):
        raise AuthorizationError("Administrator privileges required")
    return user


def get_audit_service(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_uow)],
) -> AuditService:
    """Return an AuditService bound to a fresh session."""
    uow.__enter__()
    try:
        return AuditService(uow.audit_logs)
    finally:
        # Session lifetime is managed by the caller via context manager; we
        # deliberately do not close here as the same session is reused.
        pass


def get_notification_service(
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_uow)],
) -> NotificationService:
    """Return a NotificationService bound to a fresh session."""
    uow.__enter__()
    return NotificationService(uow.notifications)
```

### backend/app/api/routers/__init__.py

```python
"""FastAPI routers."""

from app.api.routers.auth import router as auth_router
from app.api.routers.health import router as health_router
from app.api.routers.organizations import router as organizations_router
from app.api.routers.users import router as users_router

__all__ = [
    "auth_router",
    "health_router",
    "organizations_router",
    "users_router",
]
```

### backend/app/api/routers/health.py

```python
"""Health check endpoints."""

from __future__ import annotations

from fastapi import APIRouter, status
from sqlalchemy import text

from app.api.schemas.common import HealthResponse
from app.core.config import settings
from app.infrastructure.persistence.database import get_engine

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
)
def liveness() -> HealthResponse:
    """Return the service liveness status."""
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )


@router.get(
    "/health/ready",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
)
def readiness() -> HealthResponse:
    """Return the service readiness status by validating DB connectivity."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return HealthResponse(
        status="ready",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )
```

### backend/app/api/routers/auth.py

```python
"""Authentication endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_current_user
from app.application.dtos.auth import RefreshTokenDTO, TokenDTO
from app.application.dtos.user import UserDTO
from app.application.mappers import user_to_dto
from app.application.use_cases.auth import (
    LoginCommand,
    LoginUseCase,
    RefreshTokenCommand,
    RefreshTokenUseCase,
)
from app.domain.entities.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and obtain access + refresh tokens",
)
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenDTO:
    """Authenticate a user with email + password (OAuth2 password flow compatible)."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    use_case = LoginUseCase()
    return use_case.execute(
        LoginCommand(
            email=form_data.username,
            password=form_data.password,
            ip_address=ip,
            user_agent=ua,
        )
    )


@router.post(
    "/refresh",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="Exchange a refresh token for a new access token",
)
def refresh_token(payload: RefreshTokenDTO) -> TokenDTO:
    """Refresh an access token using a valid refresh token."""
    use_case = RefreshTokenUseCase()
    return use_case.execute(RefreshTokenCommand(refresh_token=payload.refresh_token))


@router.get(
    "/me",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    summary="Return the authenticated user",
)
def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserDTO:
    """Return the currently authenticated user."""
    return user_to_dto(current_user)
```

### backend/app/api/routers/organizations.py

```python
"""Organization endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.organization import (
    OrganizationCreateDTO,
    OrganizationDTO,
    OrganizationUpdateDTO,
)
from app.application.use_cases.organizations import (
    CreateOrganizationCommand,
    CreateOrganizationUseCase,
    GetOrganizationQuery,
    GetOrganizationUseCase,
    ListOrganizationsQuery,
    ListOrganizationsUseCase,
    UpdateOrganizationCommand,
    UpdateOrganizationUseCase,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post(
    "",
    response_model=OrganizationDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new organization",
)
def create_organization(
    payload: OrganizationCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> OrganizationDTO:
    """Create a new organization."""
    use_case = CreateOrganizationUseCase()
    return use_case.execute(
        CreateOrganizationCommand(
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            billing_email=str(payload.billing_email) if payload.billing_email else None,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[OrganizationDTO],
    status_code=status.HTTP_200_OK,
    summary="List organizations",
)
def list_organizations(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[OrganizationDTO]:
    """List organizations visible to the caller."""
    use_case = ListOrganizationsUseCase()
    return use_case.execute(
        ListOrganizationsQuery(
            page=PageDTO(limit=limit, offset=offset),
            context=context,
        )
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve an organization by ID",
)
def get_organization(
    organization_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> OrganizationDTO:
    """Retrieve an organization."""
    use_case = GetOrganizationUseCase()
    return use_case.execute(
        GetOrganizationQuery(organization_id=organization_id, context=context)
    )


@router.patch(
    "/{organization_id}",
    response_model=OrganizationDTO,
    status_code=status.HTTP_200_OK,
    summary="Update an organization",
)
def update_organization(
    organization_id: UUID,
    payload: OrganizationUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> OrganizationDTO:
    """Update an organization."""
    use_case = UpdateOrganizationUseCase()
    return use_case.execute(
        UpdateOrganizationCommand(
            organization_id=organization_id,
            name=payload.name,
            description=payload.description,
            billing_email=str(payload.billing_email) if payload.billing_email else None,
            is_active=payload.is_active,
            context=context,
        )
    )
```

### backend/app/api/routers/users.py

```python
"""User endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.user import UserCreateDTO, UserDTO, UserUpdateDTO
from app.application.mappers import user_to_dto
from app.application.use_cases.auth import RegisterCommand, RegisterUseCase
from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.domain.enums import UserRole, UserStatus
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Email
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user (admin operation)",
)
def create_user(
    payload: UserCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Admin-only endpoint to create a new user."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_users(context.actor),
        "You do not have permission to create users",
    )
    org_id = payload.organization_id or context.actor.organization_id
    if org_id is not None:
        AuthorizationDomainService.ensure_same_organization(context.actor, org_id)

    use_case = RegisterUseCase()
    return use_case.execute(
        RegisterCommand(
            email=str(payload.email),
            password=payload.password,
            full_name=payload.full_name,
            organization_id=org_id,
            role=payload.role,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[UserDTO],
    status_code=status.HTTP_200_OK,
    summary="List users in the caller's organization",
)
def list_users(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    role: UserRole | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
) -> PaginatedResultDTO[UserDTO]:
    """List users in the caller's organization."""
    if context.organization_id is None:
        return PaginatedResultDTO[UserDTO](items=[], total=0, limit=limit, offset=offset)

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        if search:
            items = uow.users.search(context.organization_id, search, page)
        elif role is not None:
            items = uow.users.list_by_role(context.organization_id, role.value, page)
        else:
            items = uow.users.list_by_organization(context.organization_id, page)
        total = uow.users.count_by_organization(context.organization_id)

    return PaginatedResultDTO[UserDTO](
        items=[user_to_dto(u) for u in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{user_id}",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a user by ID",
)
def get_user(
    user_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Retrieve a user."""
    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, user.organization_id
        )
        return user_to_dto(user)


@router.patch(
    "/{user_id}",
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
)
def update_user(
    user_id: UUID,
    payload: UserUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Update a user's profile, role, or status."""
    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found")

        AuthorizationDomainService.ensure_same_organization(
            context.actor, user.organization_id
        )

        if payload.role is not None or payload.status is not None:
            AuthorizationDomainService.ensure(
                AuthorizationDomainService.can_manage_users(context.actor),
                "You do not have permission to change user role or status",
            )

        if payload.full_name is not None:
            user.full_name = payload.full_name
            user.touch()
        if payload.role is not None:
            user.change_role(payload.role)
        if payload.status is not None:
            if payload.status == UserStatus.ACTIVE:
                user.activate()
            elif payload.status == UserStatus.SUSPENDED:
                user.suspend()
            elif payload.status == UserStatus.DEACTIVATED:
                user.deactivate()

        updated = uow.users.update(user)
        uow.commit()
        return user_to_dto(updated)


@router.post(
    "/invite",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Invite a new user to the caller's organization",
)
def invite_user(
    payload: UserCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> UserDTO:
    """Invite a new user by creating an invited account."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_users(context.actor),
        "You do not have permission to invite users",
    )
    if context.organization_id is None:
        raise ConflictError("Inviting requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        if uow.users.email_exists(str(payload.email)):
            raise ConflictError(f"Email {payload.email} is already registered")

        from app.domain.entities.user import User

        user = User(
            email=Email(str(payload.email)),
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
            organization_id=context.organization_id,
            role=payload.role,
            status=UserStatus.INVITED,
            is_email_verified=False,
        )
        created = uow.users.add(user)
        uow.commit()
        return user_to_dto(created)
```

### backend/app/api/routers/teams.py

```python
"""Team endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.organization import TeamCreateDTO, TeamDTO, TeamUpdateDTO
from app.application.mappers import team_to_dto
from app.core.exceptions import ConflictError, NotFoundError
from app.domain.entities.organization import Team
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post(
    "",
    response_model=TeamDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a team in the caller's organization",
)
def create_team(
    payload: TeamCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Create a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to create teams",
    )
    if context.organization_id is None:
        raise ConflictError("Team creation requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        if uow.teams.slug_exists(context.organization_id, payload.slug):
            raise ConflictError(f"Team slug '{payload.slug}' is already in use")

        team = Team(
            organization_id=context.organization_id,
            name=payload.name,
            slug=Slug(payload.slug),
            description=payload.description,
        )
        created = uow.teams.add(team)
        uow.commit()
        return team_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[TeamDTO],
    status_code=status.HTTP_200_OK,
    summary="List teams in the caller's organization",
)
def list_teams(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[TeamDTO]:
    """List teams in the organization."""
    if context.organization_id is None:
        return PaginatedResultDTO[TeamDTO](items=[], total=0, limit=limit, offset=offset)

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        items = uow.teams.list_by_organization(context.organization_id, page)
        total = uow.teams.count_by_organization(context.organization_id)

    return PaginatedResultDTO[TeamDTO](
        items=[team_to_dto(t) for t in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{team_id}",
    response_model=TeamDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a team",
)
def get_team(
    team_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Retrieve a team."""
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        return team_to_dto(team)


@router.patch(
    "/{team_id}",
    response_model=TeamDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a team",
)
def update_team(
    team_id: UUID,
    payload: TeamUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Update a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to update teams",
    )
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )

        if payload.name is not None:
            team.rename(payload.name)
        if payload.description is not None:
            team.description = payload.description
            team.touch()

        updated = uow.teams.update(team)
        uow.commit()
        return team_to_dto(updated)


@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete (soft) a team",
)
def delete_team(
    team_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> None:
    """Soft-delete a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to delete teams",
    )
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        uow.teams.delete(team_id)
        uow.commit()
```

### backend/app/api/routers/projects.py

```python
"""Project endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.project import ProjectCreateDTO, ProjectDTO, ProjectUpdateDTO
from app.application.mappers import project_to_dto
from app.core.exceptions import ConflictError, NotFoundError
from app.domain.entities.project import Project
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
)
def create_project(
    payload: ProjectCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Create a new project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to create projects",
    )
    if context.organization_id is None:
        raise ConflictError("Project creation requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(payload.team_id)
        if team is None:
            raise NotFoundError(f"Team {payload.team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        if uow.projects.key_exists(context.organization_id, payload.key):
            raise ConflictError(f"Project key '{payload.key}' is already in use")
        if uow.projects.slug_exists(context.organization_id, payload.slug):
            raise ConflictError(f"Project slug '{payload.slug}' is already in use")

        project = Project(
            organization_id=context.organization_id,
            team_id=payload.team_id,
            name=payload.name,
            key=payload.key,
            slug=Slug(payload.slug),
            description=payload.description,
            start_date=payload.start_date,
            target_end_date=payload.target_end_date,
        )
        created = uow.projects.add(project)
        uow.commit()
        return project_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[ProjectDTO],
    status_code=status.HTTP_200_OK,
    summary="List projects",
)
def list_projects(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    team_id: UUID | None = Query(default=None),
    include_archived: bool = Query(default=False),
) -> PaginatedResultDTO[ProjectDTO]:
    """List projects."""
    if context.organization_id is None:
        return PaginatedResultDTO[ProjectDTO](
            items=[], total=0, limit=limit, offset=offset
        )

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        if team_id is not None:
            team = uow.teams.get_by_id(team_id)
            if team is None:
                raise NotFoundError(f"Team {team_id} not found")
            AuthorizationDomainService.ensure_same_organization(
                context.actor, team.organization_id
            )
            items = uow.projects.list_by_team(team_id, page, include_archived)
        else:
            items = uow.projects.list_by_organization(
                context.organization_id, page, include_archived
            )
        total = uow.projects.count_by_organization(
            context.organization_id, include_archived
        )

    return PaginatedResultDTO[ProjectDTO](
        items=[project_to_dto(p) for p in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a project",
)
def get_project(
    project_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Retrieve a project."""
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        return project_to_dto(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a project",
)
def update_project(
    project_id: UUID,
    payload: ProjectUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Update a project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to update projects",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        if payload.name is not None:
            project.rename(payload.name)
        if payload.description is not None:
            project.description = payload.description
            project.touch()
        if payload.start_date is not None:
            project.start_date = payload.start_date
            project.touch()
        if payload.target_end_date is not None:
            project.target_end_date = payload.target_end_date
            project.touch()
        if payload.is_archived is not None:
            if payload.is_archived:
                project.archive()
            else:
                project.unarchive()

        updated = uow.projects.update(project)
        uow.commit()
        return project_to_dto(updated)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete (soft) a project",
)
def delete_project(
    project_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> None:
    """Soft-delete a project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to delete projects",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        uow.projects.delete(project_id)
        uow.commit()
```

### backend/app/api/routers/sprints.py

```python
"""Sprint endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.sprint import (
    SprintCompleteDTO,
    SprintCreateDTO,
    SprintDTO,
    SprintUpdateDTO,
)
from app.application.mappers import sprint_to_dto
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.entities.sprint import Sprint
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.post(
    "",
    response_model=SprintDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a sprint",
)
def create_sprint(
    payload: SprintCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Create a new sprint."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to create sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(payload.project_id)
        if project is None:
            raise NotFoundError(f"Project {payload.project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        sprint = Sprint(
            project_id=payload.project_id,
            name=payload.name,
            goal=payload.goal,
            start_date=payload.start_date,
            end_date=payload.end_date,
            planned_capacity=payload.planned_capacity,
        )
        created = uow.sprints.add(sprint)
        uow.commit()
        return sprint_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[SprintDTO],
    status_code=status.HTTP_200_OK,
    summary="List sprints for a project",
)
def list_sprints(
    context: Annotated[RequestContext, Depends(get_request_context)],
    project_id: UUID = Query(...),
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[SprintDTO]:
    """List sprints in a project."""
    page = PageRequest(limit=limit, offset=offset, order_by="start_date")
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        items = uow.sprints.list_by_project(project_id, page)
        from app.domain.repositories.specifications import SprintFilter

        total = uow.sprints.count(SprintFilter(project_id=project_id))

    return PaginatedResultDTO[SprintDTO](
        items=[sprint_to_dto(s) for s in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{sprint_id}",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a sprint",
)
def get_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Retrieve a sprint."""
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        return sprint_to_dto(sprint)


@router.patch(
    "/{sprint_id}",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a sprint",
)
def update_sprint(
    sprint_id: UUID,
    payload: SprintUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Update sprint fields."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to update sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        if payload.name is not None:
            sprint.name = payload.name
        if payload.goal is not None:
            sprint.goal = payload.goal
        if payload.start_date is not None:
            sprint.start_date = payload.start_date
        if payload.end_date is not None:
            sprint.end_date = payload.end_date
        if payload.planned_capacity is not None:
            sprint.planned_capacity = payload.planned_capacity
        sprint.touch()

        if sprint.end_date < sprint.start_date:
            raise BusinessRuleViolationError("end_date cannot be before start_date")

        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.post(
    "/{sprint_id}/start",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Start a sprint",
)
def start_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Transition a sprint into the active state."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to start sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        if uow.sprints.get_active_for_project(sprint.project_id) is not None:
            raise BusinessRuleViolationError(
                "Another sprint is already active in this project"
            )
        sprint.start()
        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.post(
    "/{sprint_id}/complete",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Complete a sprint",
)
def complete_sprint(
    sprint_id: UUID,
    payload: SprintCompleteDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Mark a sprint as completed with a final velocity."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to complete sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        sprint.complete(payload.completed_points)
        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.delete(
    "/{sprint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete (soft) a sprint",
)
def delete_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> None:
    """Soft-delete a sprint."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to delete sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        uow.sprints.delete(sprint_id)
        uow.commit()
```

### backend/app/api/main.py

```python
"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import register_exception_handlers
from app.api.routers.auth import router as auth_router
from app.api.routers.health import router as health_router
from app.api.routers.organizations import router as organizations_router
from app.api.routers.projects import router as projects_router
from app.api.routers.sprints import router as sprints_router
from app.api.routers.teams import router as teams_router
from app.api.routers.users import router as users_router
from app.core.config import settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(health_router, prefix=settings.API_V1_PREFIX)
    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(organizations_router, prefix=settings.API_V1_PREFIX)
    app.include_router(teams_router, prefix=settings.API_V1_PREFIX)
    app.include_router(users_router, prefix=settings.API_V1_PREFIX)
    app.include_router(projects_router, prefix=settings.API_V1_PREFIX)
    app.include_router(sprints_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
```

================================================================================

### backend/app/domain/entities/session.py

```python
"""User session entity for refresh-token lifecycle management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import ValidationError
from app.domain.entities.base import Entity


@dataclass
class UserSession(Entity):
    """A persistent user session backing a refresh token."""

    user_id: UUID = field(default_factory=lambda: UUID(int=0))
    refresh_token_hash: str = ""
    issued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    revoked_at: datetime | None = None
    replaced_by_session_id: UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    last_used_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.refresh_token_hash:
            raise ValidationError("refresh_token_hash is required")
        if self.expires_at <= self.issued_at:
            raise ValidationError("Session expires_at must be after issued_at")

    @property
    def is_active(self) -> bool:
        now = datetime.now(timezone.utc)
        return self.revoked_at is None and self.expires_at > now

    def revoke(self, replaced_by: UUID | None = None) -> None:
        if self.revoked_at is None:
            self.revoked_at = datetime.now(timezone.utc)
            self.replaced_by_session_id = replaced_by
            self.touch()

    def record_use(self) -> None:
        self.last_used_at = datetime.now(timezone.utc)
        self.touch()
```

### backend/app/domain/repositories/session_repository.py

```python
"""Repository contract for the UserSession aggregate."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence
from uuid import UUID

from app.domain.entities.session import UserSession
from app.domain.repositories.base import Repository
from app.domain.repositories.specifications import PageRequest


class UserSessionRepositoryContract(Repository[UserSession], ABC):
    """Repository contract for user sessions."""

    @abstractmethod
    def get_by_token_hash(self, token_hash: str) -> UserSession | None:
        """Return a session by its refresh-token hash."""

    @abstractmethod
    def list_active_by_user(self, user_id: UUID) -> Sequence[UserSession]:
        """Return all active sessions for a user."""

    @abstractmethod
    def list_by_user(
        self, user_id: UUID, page: PageRequest
    ) -> Sequence[UserSession]:
        """Return all sessions for a user (active or revoked)."""

    @abstractmethod
    def revoke_all_for_user(self, user_id: UUID) -> int:
        """Revoke every active session for a user. Returns count revoked."""

    @abstractmethod
    def purge_expired(self, cutoff: datetime) -> int:
        """Delete sessions expired before the cutoff. Returns count purged."""
```

### backend/app/domain/services/password_policy.py

```python
"""Password policy enforcement."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.exceptions import ValidationError

_UPPER_RE = re.compile(r"[A-Z]")
_LOWER_RE = re.compile(r"[a-z]")
_DIGIT_RE = re.compile(r"\d")
_SPECIAL_RE = re.compile(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]")


@dataclass(frozen=True)
class PasswordPolicy:
    """Configurable password policy rules."""

    min_length: int = 8
    max_length: int = 128
    require_upper: bool = True
    require_lower: bool = True
    require_digit: bool = True
    require_special: bool = False
    forbid_whitespace: bool = True

    def validate(self, password: str) -> None:
        """Validate a plaintext password. Raises ValidationError when invalid."""
        if not isinstance(password, str):
            raise ValidationError("Password must be a string")
        if len(password) < self.min_length:
            raise ValidationError(
                f"Password must be at least {self.min_length} characters long"
            )
        if len(password) > self.max_length:
            raise ValidationError(
                f"Password must be at most {self.max_length} characters long"
            )
        if self.forbid_whitespace and any(ch.isspace() for ch in password):
            raise ValidationError("Password must not contain whitespace characters")
        if self.require_upper and not _UPPER_RE.search(password):
            raise ValidationError("Password must contain an uppercase letter")
        if self.require_lower and not _LOWER_RE.search(password):
            raise ValidationError("Password must contain a lowercase letter")
        if self.require_digit and not _DIGIT_RE.search(password):
            raise ValidationError("Password must contain a digit")
        if self.require_special and not _SPECIAL_RE.search(password):
            raise ValidationError("Password must contain a special character")


DEFAULT_PASSWORD_POLICY = PasswordPolicy()
```

### backend/app/domain/services/permissions.py

```python
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
```

### backend/app/infrastructure/persistence/models/session.py

```python
"""ORM model for UserSession."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class UserSessionModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Persistent user session backing a refresh token."""

    __tablename__ = "user_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    refresh_token_hash: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True, index=True
    )
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    replaced_by_session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
```

### backend/app/infrastructure/persistence/repositories/session_repository.py

```python
"""SQLAlchemy implementation of the UserSession repository."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.domain.entities.session import UserSession
from app.domain.repositories.session_repository import UserSessionRepositoryContract
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.models.session import UserSessionModel
from app.infrastructure.persistence.repositories._base import apply_pagination, utcnow


class SQLAlchemyUserSessionRepository(UserSessionRepositoryContract):
    """SQLAlchemy implementation of the UserSession repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def _to_entity(self, m: UserSessionModel) -> UserSession:
        return UserSession(
            id=m.id,
            created_at=m.created_at,
            updated_at=m.updated_at,
            user_id=m.user_id,
            refresh_token_hash=m.refresh_token_hash,
            issued_at=m.issued_at,
            expires_at=m.expires_at,
            revoked_at=m.revoked_at,
            replaced_by_session_id=m.replaced_by_session_id,
            ip_address=m.ip_address,
            user_agent=m.user_agent,
            last_used_at=m.last_used_at,
        )

    def _to_model(
        self, e: UserSession, m: UserSessionModel | None = None
    ) -> UserSessionModel:
        m = m or UserSessionModel()
        m.id = e.id
        m.user_id = e.user_id
        m.refresh_token_hash = e.refresh_token_hash
        m.issued_at = e.issued_at
        m.expires_at = e.expires_at
        m.revoked_at = e.revoked_at
        m.replaced_by_session_id = e.replaced_by_session_id
        m.ip_address = e.ip_address
        m.user_agent = e.user_agent
        m.last_used_at = e.last_used_at
        return m

    def get_by_id(self, entity_id: UUID) -> UserSession | None:
        model = self._session.get(UserSessionModel, entity_id)
        return self._to_entity(model) if model else None

    def add(self, entity: UserSession) -> UserSession:
        model = self._to_model(entity)
        self._session.add(model)
        self._session.flush()
        return self._to_entity(model)

    def update(self, entity: UserSession) -> UserSession:
        model = self._session.get(UserSessionModel, entity.id)
        if model is None:
            raise NotFoundError(f"UserSession {entity.id} not found")
        self._to_model(entity, model)
        self._session.flush()
        return self._to_entity(model)

    def delete(self, entity_id: UUID) -> None:
        model = self._session.get(UserSessionModel, entity_id)
        if model is None:
            raise NotFoundError(f"UserSession {entity_id} not found")
        self._session.delete(model)
        self._session.flush()

    def exists(self, entity_id: UUID) -> bool:
        stmt = select(func.count()).select_from(UserSessionModel).where(
            UserSessionModel.id == entity_id
        )
        return int(self._session.execute(stmt).scalar_one() or 0) > 0

    def get_by_token_hash(self, token_hash: str) -> UserSession | None:
        stmt = select(UserSessionModel).where(
            UserSessionModel.refresh_token_hash == token_hash
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return self._to_entity(model) if model else None

    def list_active_by_user(self, user_id: UUID) -> Sequence[UserSession]:
        now = utcnow()
        stmt = (
            select(UserSessionModel)
            .where(
                UserSessionModel.user_id == user_id,
                UserSessionModel.revoked_at.is_(None),
                UserSessionModel.expires_at > now,
            )
            .order_by(UserSessionModel.created_at.desc())
        )
        return [self._to_entity(m) for m in self._session.execute(stmt).scalars()]

    def list_by_user(
        self, user_id: UUID, page: PageRequest
    ) -> Sequence[UserSession]:
        stmt = select(UserSessionModel).where(UserSessionModel.user_id == user_id)
        stmt = apply_pagination(stmt, page, UserSessionModel.created_at)
        return [self._to_entity(m) for m in self._session.execute(stmt).scalars()]

    def revoke_all_for_user(self, user_id: UUID) -> int:
        now = utcnow()
        stmt = select(UserSessionModel).where(
            UserSessionModel.user_id == user_id,
            UserSessionModel.revoked_at.is_(None),
        )
        models = list(self._session.execute(stmt).scalars())
        for model in models:
            model.revoked_at = now
        self._session.flush()
        return len(models)

    def purge_expired(self, cutoff: datetime) -> int:
        stmt = delete(UserSessionModel).where(UserSessionModel.expires_at < cutoff)
        result = self._session.execute(stmt)
        return int(result.rowcount or 0)
```

### backend/app/infrastructure/security/__init__.py

```python
"""Security infrastructure utilities."""

from app.infrastructure.security.token_hasher import hash_token, verify_token_hash

__all__ = ["hash_token", "verify_token_hash"]
```

### backend/app/infrastructure/security/token_hasher.py

```python
"""Deterministic token hashing for refresh-token storage."""

from __future__ import annotations

import hashlib
import hmac

from app.core.config import settings


def hash_token(token: str) -> str:
    """Return a deterministic HMAC-SHA256 hex digest of a token."""
    if not token:
        raise ValueError("token must not be empty")
    digest = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    )
    return digest.hexdigest()


def verify_token_hash(token: str, expected_hash: str) -> bool:
    """Constant-time comparison of a token against its stored hash."""
    return hmac.compare_digest(hash_token(token), expected_hash)
```

### backend/app/application/dtos/auth_extended.py

```python
"""Extended authentication DTOs (password change, session listing, logout)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LogoutDTO(BaseModel):
    """Payload for logging out a specific session."""

    refresh_token: str = Field(min_length=1)


class LogoutAllDTO(BaseModel):
    """Empty payload marker for logging out of all sessions."""

    model_config = ConfigDict(frozen=True)


class ChangePasswordDTO(BaseModel):
    """Payload for changing the current user's password."""

    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UserSessionDTO(BaseModel):
    """User session response DTO."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    issued_at: datetime
    expires_at: datetime
    revoked_at: datetime | None
    ip_address: str | None
    user_agent: str | None
    last_used_at: datetime | None
    created_at: datetime
```

### backend/app/application/use_cases/auth/logout.py

```python
"""Logout use cases."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.use_cases.base import UseCase
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.infrastructure.security.token_hasher import hash_token


@dataclass(frozen=True)
class LogoutCommand:
    """Logout a single session identified by its refresh token."""

    refresh_token: str


class LogoutUseCase(UseCase[LogoutCommand, None]):
    """Revoke the session tied to a refresh token."""

    def execute(self, command: LogoutCommand) -> None:
        payload = decode_token(command.refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Provided token is not a refresh token")

        token_hash = hash_token(command.refresh_token)
        with self._uow_factory() as uow:
            session = uow.user_sessions.get_by_token_hash(token_hash)
            if session is not None and session.is_active:
                session.revoke()
                uow.user_sessions.update(session)
                uow.commit()


@dataclass(frozen=True)
class LogoutAllCommand:
    """Revoke every active session for a user."""

    user_id: UUID


class LogoutAllUseCase(UseCase[LogoutAllCommand, int]):
    """Revoke every active session for a given user."""

    def execute(self, command: LogoutAllCommand) -> int:
        with self._uow_factory() as uow:
            count = uow.user_sessions.revoke_all_for_user(command.user_id)
            uow.commit()
            return count
```

### backend/app/application/use_cases/auth/change_password.py

```python
"""Change password use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.use_cases.base import UseCase
from app.core.exceptions import AuthenticationError, NotFoundError
from app.core.security import hash_password, verify_password
from app.domain.services.password_policy import DEFAULT_PASSWORD_POLICY, PasswordPolicy


@dataclass(frozen=True)
class ChangePasswordCommand:
    """Change password command."""

    user_id: UUID
    current_password: str
    new_password: str


class ChangePasswordUseCase(UseCase[ChangePasswordCommand, None]):
    """Change a user's password after verifying their current one."""

    def __init__(self, policy: PasswordPolicy = DEFAULT_PASSWORD_POLICY) -> None:
        super().__init__()
        self._policy = policy

    def execute(self, command: ChangePasswordCommand) -> None:
        self._policy.validate(command.new_password)

        with self._uow_factory() as uow:
            user = uow.users.get_by_id(command.user_id)
            if user is None:
                raise NotFoundError(f"User {command.user_id} not found")
            if not verify_password(command.current_password, user.hashed_password):
                raise AuthenticationError("Current password is incorrect")
            if verify_password(command.new_password, user.hashed_password):
                raise AuthenticationError(
                    "New password must be different from the current password"
                )

            user.hashed_password = hash_password(command.new_password)
            user.touch()
            uow.users.update(user)
            uow.user_sessions.revoke_all_for_user(command.user_id)
            uow.commit()
```

### backend/app/application/services/authentication_service.py

```python
"""Application service that coordinates authentication flows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.domain.entities.session import UserSession
from app.domain.entities.user import User
from app.domain.enums import UserStatus
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork
from app.infrastructure.security.token_hasher import hash_token


@dataclass(frozen=True)
class AuthenticationResult:
    """Result of a successful authentication."""

    user: User
    access_token: str
    refresh_token: str
    expires_in: int


class AuthenticationService:
    """Orchestrates login, refresh, and session persistence."""

    def __init__(
        self, uow_factory: type[SQLAlchemyUnitOfWork] = SQLAlchemyUnitOfWork
    ) -> None:
        self._uow_factory = uow_factory

    def _issue(
        self,
        user: User,
        ip_address: str | None,
        user_agent: str | None,
        previous_session_id: UUID | None = None,
    ) -> AuthenticationResult:
        access_token = create_access_token(
            subject=user.id,
            additional_claims={
                "role": user.role.value,
                "org": str(user.organization_id) if user.organization_id else None,
            },
        )
        refresh_token = create_refresh_token(subject=user.id)
        now = datetime.now(timezone.utc)
        session = UserSession(
            user_id=user.id,
            refresh_token_hash=hash_token(refresh_token),
            issued_at=now,
            expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        with self._uow_factory() as uow:
            uow.user_sessions.add(session)
            if previous_session_id is not None:
                prev = uow.user_sessions.get_by_id(previous_session_id)
                if prev is not None and prev.is_active:
                    prev.revoke(replaced_by=session.id)
                    uow.user_sessions.update(prev)
            user.record_login(now)
            uow.users.update(user)
            uow.commit()

        return AuthenticationResult(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def login(
        self,
        email: str,
        password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuthenticationResult:
        with self._uow_factory() as uow:
            user = uow.users.get_by_email(email)
            if user is None or not verify_password(password, user.hashed_password):
                raise AuthenticationError("Invalid email or password")
            if user.status != UserStatus.ACTIVE:
                raise AuthenticationError(
                    f"Account is not active (status: {user.status.value})"
                )
        return self._issue(user, ip_address, user_agent)

    def refresh(
        self,
        refresh_token: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuthenticationResult:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Provided token is not a refresh token")

        subject = payload.get("sub")
        if not subject:
            raise AuthenticationError("Refresh token missing subject")
        try:
            user_id = UUID(subject)
        except ValueError as exc:
            raise AuthenticationError("Invalid subject in token") from exc

        token_hash = hash_token(refresh_token)
        with self._uow_factory() as uow:
            session = uow.user_sessions.get_by_token_hash(token_hash)
            if session is None:
                raise AuthenticationError("Session not found for this refresh token")
            if not session.is_active:
                raise AuthenticationError("Refresh token has been revoked or expired")
            if session.user_id != user_id:
                raise AuthenticationError("Refresh token does not match session owner")

            user = uow.users.get_by_id(user_id)
            if user is None or user.status != UserStatus.ACTIVE:
                raise AuthenticationError("User is not active")

            session.record_use()
            uow.user_sessions.update(session)
            uow.commit()

        return self._issue(user, ip_address, user_agent, previous_session_id=session.id)

    def logout(self, refresh_token: str) -> None:
        token_hash = hash_token(refresh_token)
        with self._uow_factory() as uow:
            session = uow.user_sessions.get_by_token_hash(token_hash)
            if session is not None and session.is_active:
                session.revoke()
                uow.user_sessions.update(session)
                uow.commit()

    def logout_all(self, user_id: UUID) -> int:
        with self._uow_factory() as uow:
            count = uow.user_sessions.revoke_all_for_user(user_id)
            uow.commit()
            return count
```

### backend/app/api/security.py

```python
"""API-layer security dependencies for authentication and authorization."""

from __future__ import annotations

from typing import Annotated, Callable
from uuid import UUID

from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer

from app.application.context import RequestContext
from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token
from app.domain.entities.user import User
from app.domain.enums import UserRole
from app.domain.services.permissions import Permission, PermissionRegistry
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False,
)


def _extract_bearer(request: Request, token: str | None) -> str:
    if token:
        return token
    header = request.headers.get("authorization")
    if header and header.lower().startswith("bearer "):
        return header.split(" ", 1)[1].strip()
    raise AuthenticationError("Authentication credentials were not provided")


def get_authenticated_user(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
) -> User:
    """Resolve the currently authenticated user from a Bearer access token."""
    raw = _extract_bearer(request, token)
    payload = decode_token(raw)
    if payload.get("type") != "access":
        raise AuthenticationError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise AuthenticationError("Token missing subject")

    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise AuthenticationError("Invalid subject in token") from exc

    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise AuthenticationError("User not found")
        if not user.is_active:
            raise AuthenticationError("User account is not active")

    request.state.current_user = user
    return user


def build_request_context(
    request: Request,
    user: Annotated[User, Depends(get_authenticated_user)],
    x_forwarded_for: Annotated[str | None, Header(alias="X-Forwarded-For")] = None,
) -> RequestContext:
    """Build a RequestContext for downstream use cases."""
    ip_address = x_forwarded_for or (request.client.host if request.client else None)
    user_agent = request.headers.get("user-agent")
    return RequestContext(actor=user, ip_address=ip_address, user_agent=user_agent)


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    """Dependency factory: require the current user to hold one of the given roles."""

    def _dep(user: Annotated[User, Depends(get_authenticated_user)]) -> User:
        if user.role not in roles:
            allowed = ", ".join(r.value for r in roles)
            raise AuthorizationError(f"This action requires one of: {allowed}")
        return user

    return _dep


def require_permissions(*permissions: Permission) -> Callable[[User], User]:
    """Dependency factory: require the caller to have every listed permission."""

    def _dep(user: Annotated[User, Depends(get_authenticated_user)]) -> User:
        for permission in permissions:
            PermissionRegistry.ensure(user, permission)
        return user

    return _dep


def require_any_permission(*permissions: Permission) -> Callable[[User], User]:
    """Dependency factory: require the caller to have at least one listed permission."""

    def _dep(user: Annotated[User, Depends(get_authenticated_user)]) -> User:
        PermissionRegistry.ensure_any(user, *permissions)
        return user

    return _dep
```

### backend/app/api/middleware/__init__.py

```python
"""API middleware."""

from app.api.middleware.authentication import AuthenticationMiddleware
from app.api.middleware.request_context import RequestContextMiddleware

__all__ = ["AuthenticationMiddleware", "RequestContextMiddleware"]
```

### backend/app/api/middleware/authentication.py

```python
"""Optional authentication middleware.

This middleware attempts to attach the current user to `request.state` when a
valid Bearer token is present. It never rejects a request on its own — route
dependencies remain the source of truth for enforcement. This design keeps
public routes (health, login, refresh, docs) unaffected while enabling
downstream code (e.g., audit logging) to access the caller when available.
"""

from __future__ import annotations

from uuid import UUID

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger
from app.core.security import decode_token
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

_logger = get_logger("api.middleware.auth")


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Attach `request.state.current_user` when a valid access token is present."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.current_user = None
        header = request.headers.get("authorization")
        if header and header.lower().startswith("bearer "):
            token = header.split(" ", 1)[1].strip()
            try:
                payload = decode_token(token)
                if payload.get("type") == "access":
                    subject = payload.get("sub")
                    if subject:
                        try:
                            user_id = UUID(subject)
                        except ValueError:
                            user_id = None
                        if user_id is not None:
                            with SQLAlchemyUnitOfWork() as uow:
                                user = uow.users.get_by_id(user_id)
                            if user is not None and user.is_active:
                                request.state.current_user = user
            except Exception as exc:  # noqa: BLE001 - defensive; enforcement happens later
                _logger.debug("Ignoring invalid Authorization header: %s", exc)

        return await call_next(request)
```

### backend/app/api/middleware/request_context.py

```python
"""Request-level context middleware attaching a correlation id."""

from __future__ import annotations

from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach a stable X-Request-ID to every request/response."""

    HEADER = "X-Request-ID"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get(self.HEADER) or uuid4().hex
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[self.HEADER] = request_id
        return response
```

### backend/app/api/routers/auth_sessions.py

```python
"""Session management endpoints: refresh, logout, list active sessions."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.security import get_authenticated_user
from app.application.dtos.auth import RefreshTokenDTO, TokenDTO
from app.application.dtos.auth_extended import (
    ChangePasswordDTO,
    LogoutDTO,
    UserSessionDTO,
)
from app.application.services.authentication_service import AuthenticationService
from app.application.use_cases.auth.change_password import (
    ChangePasswordCommand,
    ChangePasswordUseCase,
)
from app.core.config import settings
from app.domain.entities.user import User
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token/refresh",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="Rotate a refresh token and issue a new access token",
)
def rotate_refresh_token(payload: RefreshTokenDTO, request: Request) -> TokenDTO:
    """Rotate a refresh token by revoking the presented one and issuing a new pair."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    service = AuthenticationService()
    result = service.refresh(payload.refresh_token, ip_address=ip, user_agent=ua)
    return TokenDTO(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        expires_in=result.expires_in,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out of the current session",
)
def logout(
    payload: LogoutDTO,
    _user: Annotated[User, Depends(get_authenticated_user)],
) -> None:
    """Revoke the session backing a refresh token."""
    service = AuthenticationService()
    service.logout(payload.refresh_token)


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out of every active session for the current user",
)
def logout_all(
    user: Annotated[User, Depends(get_authenticated_user)],
) -> None:
    """Revoke every active session for the current user."""
    service = AuthenticationService()
    service.logout_all(user.id)


@router.get(
    "/sessions",
    response_model=list[UserSessionDTO],
    status_code=status.HTTP_200_OK,
    summary="List the current user's sessions",
)
def list_sessions(
    user: Annotated[User, Depends(get_authenticated_user)],
    limit: int = 20,
    offset: int = 0,
) -> list[UserSessionDTO]:
    """Return the current user's sessions."""
    page = PageRequest(
        limit=min(max(limit, 1), settings.MAX_PAGE_SIZE),
        offset=max(offset, 0),
    )
    with SQLAlchemyUnitOfWork() as uow:
        sessions = uow.user_sessions.list_by_user(user.id, page)
    return [
        UserSessionDTO(
            id=s.id,
            user_id=s.user_id,
            issued_at=s.issued_at,
            expires_at=s.expires_at,
            revoked_at=s.revoked_at,
            ip_address=s.ip_address,
            user_agent=s.user_agent,
            last_used_at=s.last_used_at,
            created_at=s.created_at,
        )
        for s in sessions
    ]


@router.post(
    "/password/change",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change the current user's password",
)
def change_password(
    payload: ChangePasswordDTO,
    user: Annotated[User, Depends(get_authenticated_user)],
) -> None:
    """Change the current user's password and revoke all sessions."""
    use_case = ChangePasswordUseCase()
    use_case.execute(
        ChangePasswordCommand(
            user_id=user.id,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
    )
```

================================================================================

### backend/alembic.ini

```ini
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url =
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s
timezone = UTC
truncate_slug_length = 40

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %Y-%m-%dT%H:%M:%S
```

### backend/alembic/env.py

```python
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
```

### backend/alembic/script.py.mako

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from __future__ import annotations

from typing import Sequence

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: str | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
```

### backend/alembic/versions/20240101_0001_initial_schema.py

```python
"""Initial schema

Revision ID: 20240101_0001
Revises:
Create Date: 2024-01-01T00:00:00

"""
from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20240101_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(64), nullable=False),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("billing_email", sa.String(320), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_organizations_slug", "organizations", ["slug"], unique=True)
    op.create_index("ix_organizations_deleted_at", "organizations", ["deleted_at"])

    op.create_table(
        "teams",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(64), nullable=False),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("organization_id", "slug", name="uq_teams_org_slug"),
    )
    op.create_index("ix_teams_organization_id", "teams", ["organization_id"])
    op.create_index("ix_teams_deleted_at", "teams", ["deleted_at"])

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("role", sa.String(32), nullable=False, server_default="viewer"),
        sa.Column("status", sa.String(32), nullable=False, server_default="invited"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_email_verified", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_organization_id", "users", ["organization_id"])
    op.create_index("ix_users_deleted_at", "users", ["deleted_at"])

    op.create_table(
        "team_memberships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("is_lead", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("team_id", "user_id", name="uq_team_memberships_team_user"),
    )
    op.create_index("ix_team_memberships_team_id", "team_memberships", ["team_id"])
    op.create_index("ix_team_memberships_user_id", "team_memberships", ["user_id"])
    op.create_index("ix_team_memberships_deleted_at", "team_memberships", ["deleted_at"])

    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("key", sa.String(12), nullable=False),
        sa.Column("slug", sa.String(64), nullable=False),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("start_date", sa.Date, nullable=True),
        sa.Column("target_end_date", sa.Date, nullable=True),
        sa.Column("is_archived", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("organization_id", "key", name="uq_projects_org_key"),
        sa.UniqueConstraint("organization_id", "slug", name="uq_projects_org_slug"),
    )
    op.create_index("ix_projects_organization_id", "projects", ["organization_id"])
    op.create_index("ix_projects_team_id", "projects", ["team_id"])
    op.create_index("ix_projects_deleted_at", "projects", ["deleted_at"])

    op.create_table(
        "sprints",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("goal", sa.String(2000), nullable=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="planned"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("planned_capacity", sa.Integer, nullable=False, server_default="0"),
        sa.Column("completed_points", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_sprints_project_id", "sprints", ["project_id"])
    op.create_index("ix_sprints_status", "sprints", ["status"])
    op.create_index("ix_sprints_deleted_at", "sprints", ["deleted_at"])

    op.create_table(
        "work_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sprint_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("epic_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("external_key", sa.String(64), nullable=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.String(10000), nullable=True),
        sa.Column("item_type", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("priority", sa.String(32), nullable=False, server_default="medium"),
        sa.Column("story_points", sa.Integer, nullable=True),
        sa.Column("estimated_hours", sa.Float, nullable=True),
        sa.Column("actual_hours", sa.Float, nullable=True),
        sa.Column("assignee_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reporter_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "labels",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default=sa.text("'{}'::varchar[]"),
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sprint_id"], ["sprints.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["parent_id"], ["work_items.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["epic_id"], ["work_items.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["assignee_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["reporter_id"], ["users.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("project_id", "external_key", name="uq_work_items_project_external_key"),
    )
    op.create_index("ix_work_items_project_id", "work_items", ["project_id"])
    op.create_index("ix_work_items_sprint_id", "work_items", ["sprint_id"])
    op.create_index("ix_work_items_parent_id", "work_items", ["parent_id"])
    op.create_index("ix_work_items_epic_id", "work_items", ["epic_id"])
    op.create_index("ix_work_items_assignee_id", "work_items", ["assignee_id"])
    op.create_index("ix_work_items_item_type", "work_items", ["item_type"])
    op.create_index("ix_work_items_status", "work_items", ["status"])
    op.create_index("ix_work_items_deleted_at", "work_items", ["deleted_at"])

    op.create_table(
        "business_outcomes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("description", sa.String(4000), nullable=True),
        sa.Column("hypothesis", sa.String(4000), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("target_date", sa.Date, nullable=True),
        sa.Column("baseline_value", sa.Numeric(20, 6), nullable=True),
        sa.Column("target_value", sa.Numeric(20, 6), nullable=True),
        sa.Column("current_value", sa.Numeric(20, 6), nullable=True),
        sa.Column("confidence_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("financial_impact_estimate", sa.Numeric(20, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_business_outcomes_organization_id", "business_outcomes", ["organization_id"])
    op.create_index("ix_business_outcomes_status", "business_outcomes", ["status"])
    op.create_index("ix_business_outcomes_deleted_at", "business_outcomes", ["deleted_at"])

    op.create_table(
        "kpis",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("outcome_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("unit", sa.String(32), nullable=False),
        sa.Column("currency", sa.String(3), nullable=True),
        sa.Column("direction", sa.String(16), nullable=False),
        sa.Column("baseline_value", sa.Numeric(20, 6), nullable=True),
        sa.Column("target_value", sa.Numeric(20, 6), nullable=True),
        sa.Column("current_value", sa.Numeric(20, 6), nullable=True),
        sa.Column("data_source", sa.String(500), nullable=True),
        sa.Column("refresh_frequency_hours", sa.Integer, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["outcome_id"], ["business_outcomes.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_kpis_organization_id", "kpis", ["organization_id"])
    op.create_index("ix_kpis_outcome_id", "kpis", ["outcome_id"])
    op.create_index("ix_kpis_deleted_at", "kpis", ["deleted_at"])

    op.create_table(
        "metric_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("kpi_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("value", sa.Numeric(20, 6), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(200), nullable=True),
        sa.Column("notes", sa.String(2000), nullable=True),
        sa.Column("context", postgresql.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["kpi_id"], ["kpis.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_metric_snapshots_kpi_id", "metric_snapshots", ["kpi_id"])
    op.create_index("ix_metric_snapshots_recorded_at", "metric_snapshots", ["recorded_at"])
    op.create_index("ix_metric_snapshots_deleted_at", "metric_snapshots", ["deleted_at"])

    op.create_table(
        "objectives",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.String(4000), nullable=True),
        sa.Column("okr_type", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("period_start", sa.Date, nullable=False),
        sa.Column("period_end", sa.Date, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["parent_id"], ["objectives.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_objectives_organization_id", "objectives", ["organization_id"])
    op.create_index("ix_objectives_team_id", "objectives", ["team_id"])
    op.create_index("ix_objectives_status", "objectives", ["status"])
    op.create_index("ix_objectives_deleted_at", "objectives", ["deleted_at"])

    op.create_table(
        "key_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("objective_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kpi_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.String(4000), nullable=True),
        sa.Column("baseline_value", sa.Numeric(20, 6), nullable=False),
        sa.Column("target_value", sa.Numeric(20, 6), nullable=False),
        sa.Column("current_value", sa.Numeric(20, 6), nullable=False),
        sa.Column("weight", sa.Numeric(6, 3), nullable=False, server_default="1"),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["objective_id"], ["objectives.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["kpi_id"], ["kpis.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_key_results_objective_id", "key_results", ["objective_id"])
    op.create_index("ix_key_results_kpi_id", "key_results", ["kpi_id"])
    op.create_index("ix_key_results_deleted_at", "key_results", ["deleted_at"])

    op.create_table(
        "outcome_attributions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("work_item_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("sprint_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("outcome_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("kpi_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("key_result_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("attributed_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("method", sa.String(32), nullable=False),
        sa.Column("strength", sa.String(32), nullable=False),
        sa.Column("weight", sa.Numeric(6, 3), nullable=False, server_default="1"),
        sa.Column("confidence", sa.Numeric(5, 2), nullable=False, server_default="50"),
        sa.Column("estimated_value", sa.Numeric(20, 2), nullable=True),
        sa.Column("rationale", sa.String(4000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["work_item_id"], ["work_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sprint_id"], ["sprints.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["outcome_id"], ["business_outcomes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["kpi_id"], ["kpis.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["key_result_id"], ["key_results.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["attributed_by_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_outcome_attributions_organization_id", "outcome_attributions", ["organization_id"])
    op.create_index("ix_outcome_attributions_work_item_id", "outcome_attributions", ["work_item_id"])
    op.create_index("ix_outcome_attributions_sprint_id", "outcome_attributions", ["sprint_id"])
    op.create_index("ix_outcome_attributions_outcome_id", "outcome_attributions", ["outcome_id"])
    op.create_index("ix_outcome_attributions_kpi_id", "outcome_attributions", ["kpi_id"])
    op.create_index("ix_outcome_attributions_key_result_id", "outcome_attributions", ["key_result_id"])
    op.create_index("ix_outcome_attributions_strength", "outcome_attributions", ["strength"])
    op.create_index("ix_outcome_attributions_deleted_at", "outcome_attributions", ["deleted_at"])

    op.create_table(
        "evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("attribution_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("content", sa.String(10000), nullable=False),
        sa.Column("source_url", sa.String(2000), nullable=True),
        sa.Column("evidence_type", sa.String(32), nullable=False, server_default="note"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["attribution_id"], ["outcome_attributions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_evidence_attribution_id", "evidence", ["attribution_id"])
    op.create_index("ix_evidence_deleted_at", "evidence", ["deleted_at"])

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("recipient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("body", sa.String(4000), nullable=False),
        sa.Column("channel", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("subject_type", sa.String(64), nullable=True),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action_url", sa.String(2000), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.String(2000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["recipient_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_notifications_recipient_id", "notifications", ["recipient_id"])
    op.create_index("ix_notifications_organization_id", "notifications", ["organization_id"])
    op.create_index("ix_notifications_status", "notifications", ["status"])

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(32), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("ip_address", sa.String(64), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("changes", postgresql.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("metadata", postgresql.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["actor_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_audit_logs_organization_id", "audit_logs", ["organization_id"])
    op.create_index("ix_audit_logs_actor_id", "audit_logs", ["actor_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_resource_type", "audit_logs", ["resource_type"])
    op.create_index("ix_audit_logs_resource_id", "audit_logs", ["resource_id"])

    op.create_table(
        "user_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("refresh_token_hash", sa.String(128), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_by_session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("ip_address", sa.String(64), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_user_sessions_user_id", "user_sessions", ["user_id"])
    op.create_index(
        "ix_user_sessions_refresh_token_hash",
        "user_sessions",
        ["refresh_token_hash"],
        unique=True,
    )
    op.create_index("ix_user_sessions_expires_at", "user_sessions", ["expires_at"])


def downgrade() -> None:
    op.drop_table("user_sessions")
    op.drop_table("audit_logs")
    op.drop_table("notifications")
    op.drop_table("evidence")
    op.drop_table("outcome_attributions")
    op.drop_table("key_results")
    op.drop_table("objectives")
    op.drop_table("metric_snapshots")
    op.drop_table("kpis")
    op.drop_table("business_outcomes")
    op.drop_table("work_items")
    op.drop_table("sprints")
    op.drop_table("projects")
    op.drop_table("team_memberships")
    op.drop_table("users")
    op.drop_table("teams")
    op.drop_table("organizations")
```

### backend/app/core/container.py

```python
"""Dependency injection container for application-wide services and factories."""

from __future__ import annotations

from typing import Callable

from app.application.services.audit_service import AuditService
from app.application.services.authentication_service import AuthenticationService
from app.application.services.notification_service import NotificationService
from app.core.config import Settings, get_settings
from app.domain.services.attribution_service import AttributionDomainService
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.outcome_health_service import OutcomeHealthDomainService
from app.domain.services.password_policy import (
    DEFAULT_PASSWORD_POLICY,
    PasswordPolicy,
)
from app.domain.services.permissions import PermissionRegistry
from app.domain.services.sprint_metrics_service import SprintMetricsDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class Container:
    """Application service container.

    Wires up cross-cutting collaborators without introducing external DI
    frameworks. All accessors are safe to call any number of times.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._uow_factory: Callable[[], SQLAlchemyUnitOfWork] = SQLAlchemyUnitOfWork
        self._password_policy: PasswordPolicy = PasswordPolicy(
            min_length=self._settings.PASSWORD_MIN_LENGTH,
            max_length=DEFAULT_PASSWORD_POLICY.max_length,
            require_upper=DEFAULT_PASSWORD_POLICY.require_upper,
            require_lower=DEFAULT_PASSWORD_POLICY.require_lower,
            require_digit=DEFAULT_PASSWORD_POLICY.require_digit,
            require_special=DEFAULT_PASSWORD_POLICY.require_special,
            forbid_whitespace=DEFAULT_PASSWORD_POLICY.forbid_whitespace,
        )
        self._authentication_service = AuthenticationService(self._uow_factory)

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def uow_factory(self) -> Callable[[], SQLAlchemyUnitOfWork]:
        return self._uow_factory

    @property
    def password_policy(self) -> PasswordPolicy:
        return self._password_policy

    @property
    def authentication_service(self) -> AuthenticationService:
        return self._authentication_service

    @property
    def authorization(self) -> type[AuthorizationDomainService]:
        return AuthorizationDomainService

    @property
    def permissions(self) -> type[PermissionRegistry]:
        return PermissionRegistry

    @property
    def attribution(self) -> type[AttributionDomainService]:
        return AttributionDomainService

    @property
    def sprint_metrics(self) -> type[SprintMetricsDomainService]:
        return SprintMetricsDomainService

    @property
    def outcome_health(self) -> type[OutcomeHealthDomainService]:
        return OutcomeHealthDomainService

    def audit_service(self, uow: SQLAlchemyUnitOfWork) -> AuditService:
        """Build an AuditService bound to an open UnitOfWork."""
        return AuditService(uow.audit_logs)

    def notification_service(self, uow: SQLAlchemyUnitOfWork) -> NotificationService:
        """Build a NotificationService bound to an open UnitOfWork."""
        return NotificationService(uow.notifications)


_container: Container | None = None


def get_container() -> Container:
    """Return the process-wide Container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container() -> None:
    """Reset the container (used in tests)."""
    global _container
    _container = None
```

### backend/app/infrastructure/persistence/init_db.py

```python
"""Database initialization helpers."""

from __future__ import annotations

from sqlalchemy import text

from app.core.logging import get_logger
from app.infrastructure.persistence.database import get_engine
from app.infrastructure.persistence.models import Base

_logger = get_logger("infrastructure.init_db")


def ensure_extensions() -> None:
    """Ensure required PostgreSQL extensions exist."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))


def create_all() -> None:
    """Create all tables. Prefer Alembic migrations in production."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    _logger.info("Database schema created (create_all).")


def drop_all() -> None:
    """Drop all tables. Use in tests only."""
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    _logger.warning("Database schema dropped (drop_all).")


def check_connection() -> bool:
    """Return True when the database is reachable."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:  # noqa: BLE001 - health check must be defensive
        _logger.error("Database connection failed: %s", exc)
        return False


def dispose_engine() -> None:
    """Dispose the SQLAlchemy engine connection pool."""
    get_engine().dispose()
    _logger.info("Database engine disposed.")
```

### backend/app/infrastructure/persistence/transaction.py

```python
"""Transaction utilities: decorator + explicit helpers."""

from __future__ import annotations

from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Iterator, TypeVar

from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

T = TypeVar("T")


@contextmanager
def transactional() -> Iterator[SQLAlchemyUnitOfWork]:
    """Open a UnitOfWork and commit on success, rollback on error."""
    uow = SQLAlchemyUnitOfWork()
    with uow:
        try:
            yield uow
            uow.commit()
        except Exception:
            uow.rollback()
            raise


def in_transaction(func: Callable[..., T]) -> Callable[..., T]:
    """Decorate a function to run inside a UnitOfWork transaction.

    The wrapped function must accept a `uow` keyword-only argument.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        with transactional() as uow:
            return func(*args, uow=uow, **kwargs)

    return wrapper
```

### backend/app/infrastructure/seed.py

```python
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
```

### backend/app/api/lifespan.py

```python
"""FastAPI application lifespan handlers (startup / shutdown)."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.core.config import settings
from app.core.container import get_container, reset_container
from app.core.logging import configure_logging, get_logger
from app.infrastructure.persistence.init_db import check_connection, dispose_engine

_logger = get_logger("api.lifespan")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Manage startup and shutdown for the FastAPI application."""
    configure_logging()
    _logger.info(
        "Starting %s v%s (env=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )

    # Warm the DI container so misconfiguration surfaces immediately.
    get_container()

    if not check_connection():
        _logger.error("Database is not reachable at startup.")
    else:
        _logger.info("Database connection verified.")

    try:
        yield
    finally:
        _logger.info("Shutting down %s", settings.APP_NAME)
        dispose_engine()
        reset_container()
```

### backend/scripts/__init__.py

```python
"""Operational scripts."""
```

### backend/scripts/seed.py

```python
"""CLI entrypoint for seeding the database."""

from __future__ import annotations

import argparse

from app.core.logging import configure_logging, get_logger
from app.infrastructure.seed import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ORG_SLUG,
    seed_default_data,
)


def main() -> None:
    """Seed default data via the command line."""
    configure_logging()
    logger = get_logger("scripts.seed")

    parser = argparse.ArgumentParser(description="Seed default Sprint Outcome Tracer data.")
    parser.add_argument("--email", default=DEFAULT_ADMIN_EMAIL, help="Admin email")
    parser.add_argument(
        "--password", default=DEFAULT_ADMIN_PASSWORD, help="Admin password"
    )
    parser.add_argument("--slug", default=DEFAULT_ORG_SLUG, help="Organization slug")
    args = parser.parse_args()

    seed_default_data(
        admin_email=args.email,
        admin_password=args.password,
        organization_slug=args.slug,
    )
    logger.info("Seed complete.")


if __name__ == "__main__":
    main()
```

### backend/.env.example

```dotenv
# Application
APP_NAME=Sprint Business Outcome Tracer
APP_VERSION=0.1.0
ENVIRONMENT=development
DEBUG=true
API_V1_PREFIX=/api/v1

# Security (use a long, random value in production)
SECRET_KEY=change-me-to-a-long-random-secret-of-32-chars-or-more
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
PASSWORD_MIN_LENGTH=8

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=sbot
POSTGRES_PASSWORD=sbot
POSTGRES_DB=sbot
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_ECHO=false

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### backend/README.md

```markdown
# Sprint Business Outcome Tracer — Backend

Production-ready FastAPI + SQLAlchemy backend for the Sprint Business Outcome Tracer.

## Requirements

- Python 3.11+
- PostgreSQL 14+
- Redis 6+ (optional; used for future async pipelines)

## Setup

```bash
cd backend
poetry install
cp .env.example .env
```

Edit `.env` and set at minimum a strong `SECRET_KEY` (32+ characters).

## Database migrations

```bash
poetry run alembic upgrade head
```

## Seeding

```bash
poetry run python -m scripts.seed
```

Default credentials (change them immediately):

- Email: `admin@sbot.local`
- Password: `ChangeMe123!`

## Running the API

```bash
poetry run uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

Docs:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/api/v1/health
- Readiness: http://localhost:8000/api/v1/health/ready

## Architecture

The backend follows Clean Architecture:

- `app/domain` — entities, value objects, domain services, repository contracts
- `app/application` — use cases, DTOs, application services, mappers
- `app/infrastructure` — SQLAlchemy models, repository implementations, unit-of-work
- `app/api` — FastAPI routers, dependencies, middleware, exception handlers
- `app/core` — configuration, logging, security primitives, DI container

## Testing

```bash
poetry run pytest
```
```

================================================================================

### backend/app/domain/entities/work_item_extensions.py

```python
"""Extension helpers for the WorkItem aggregate.

These helpers centralize state-transition rules and derived validation used by
Work Item use cases. Behavior lives here (not inside the raw entity file) so we
avoid touching the previously-generated `WorkItem` module.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Final

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.work_item import WorkItem
from app.domain.enums import WorkItemStatus, WorkItemType


_ALLOWED_TRANSITIONS: Final[dict[WorkItemStatus, frozenset[WorkItemStatus]]] = {
    WorkItemStatus.BACKLOG: frozenset(
        {WorkItemStatus.TODO, WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED}
    ),
    WorkItemStatus.TODO: frozenset(
        {WorkItemStatus.BACKLOG, WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED}
    ),
    WorkItemStatus.IN_PROGRESS: frozenset(
        {
            WorkItemStatus.TODO,
            WorkItemStatus.IN_REVIEW,
            WorkItemStatus.DONE,
            WorkItemStatus.CANCELLED,
        }
    ),
    WorkItemStatus.IN_REVIEW: frozenset(
        {
            WorkItemStatus.IN_PROGRESS,
            WorkItemStatus.DONE,
            WorkItemStatus.CANCELLED,
        }
    ),
    WorkItemStatus.DONE: frozenset({WorkItemStatus.IN_REVIEW}),
    WorkItemStatus.CANCELLED: frozenset({WorkItemStatus.BACKLOG, WorkItemStatus.TODO}),
}


class WorkItemStateMachine:
    """Encapsulates work item status transition rules."""

    @staticmethod
    def can_transition(current: WorkItemStatus, target: WorkItemStatus) -> bool:
        if current == target:
            return False
        return target in _ALLOWED_TRANSITIONS.get(current, frozenset())

    @staticmethod
    def ensure_transition(current: WorkItemStatus, target: WorkItemStatus) -> None:
        if current == target:
            raise BusinessRuleViolationError(
                f"Work item is already in status '{current.value}'"
            )
        if target not in _ALLOWED_TRANSITIONS.get(current, frozenset()):
            raise BusinessRuleViolationError(
                f"Cannot transition work item from '{current.value}' to '{target.value}'"
            )
        if current == WorkItemStatus.DONE and target == WorkItemStatus.BACKLOG:
            raise BusinessRuleViolationError(
                "Completed work items cannot move back to backlog"
            )


def apply_status_change(item: WorkItem, target: WorkItemStatus) -> None:
    """Apply a validated status change with correct timestamp side effects."""
    WorkItemStateMachine.ensure_transition(item.status, target)

    if target == WorkItemStatus.IN_PROGRESS and item.started_at is None:
        item.started_at = datetime.now(timezone.utc)
    if target == WorkItemStatus.DONE:
        item.completed_at = datetime.now(timezone.utc)
    if item.status == WorkItemStatus.DONE and target != WorkItemStatus.DONE:
        # Reopening: clear completion timestamp
        item.completed_at = None

    item.status = target
    item.touch()


def normalize_labels(labels: list[str] | None) -> list[str]:
    """Normalize and de-duplicate labels."""
    if not labels:
        return []
    seen: list[str] = []
    for raw in labels:
        if raw is None:
            continue
        normalized = raw.strip().lower()
        if not normalized:
            continue
        if len(normalized) > 64:
            raise ValidationError("Labels must be 64 characters or fewer")
        if normalized not in seen:
            seen.append(normalized)
    return seen


def ensure_due_date_valid(due_date: date | None, target_end: date | None) -> None:
    """Optional validation for due_date against a project's target end date."""
    if due_date is None or target_end is None:
        return
    if due_date > target_end:
        raise ValidationError(
            "Due date cannot be after the project's target end date"
        )


def ensure_hierarchy(item_type: WorkItemType, epic_id, parent_id) -> None:
    """Validate parent/epic relationships based on the work-item type."""
    if item_type == WorkItemType.EPIC and epic_id is not None:
        raise ValidationError("An epic cannot belong to another epic")
    if parent_id is not None and epic_id is not None and parent_id == epic_id:
        raise ValidationError("parent_id and epic_id must not reference the same item")
```

### backend/app/application/dtos/work_item_extensions.py

```python
"""Extended DTOs for Work Item operations (assign, move, status)."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType


class WorkItemAssignDTO(BaseModel):
    """Payload for reassigning a work item."""

    assignee_id: UUID | None = None


class WorkItemStatusChangeDTO(BaseModel):
    """Payload for changing a work item's status."""

    status: WorkItemStatus
    actual_hours: float | None = Field(default=None, ge=0)


class WorkItemMoveDTO(BaseModel):
    """Payload for moving a work item to a sprint (or unassigning)."""

    sprint_id: UUID | None = None


class WorkItemReplaceDTO(BaseModel):
    """Full-replacement (PUT) payload for a work item."""

    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    item_type: WorkItemType
    priority: WorkItemPriority
    status: WorkItemStatus
    story_points: int | None = Field(default=None, ge=0, le=1000)
    estimated_hours: float | None = Field(default=None, ge=0)
    actual_hours: float | None = Field(default=None, ge=0)
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    assignee_id: UUID | None = None
    labels: list[str] = Field(default_factory=list)
    due_date: date | None = None


class WorkItemDetailDTO(BaseModel):
    """Extended read model for a work item."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    sprint_id: UUID | None
    parent_id: UUID | None
    epic_id: UUID | None
    external_key: str | None
    title: str
    description: str | None
    item_type: WorkItemType
    status: WorkItemStatus
    priority: WorkItemPriority
    story_points: int | None
    estimated_hours: float | None
    actual_hours: float | None
    assignee_id: UUID | None
    reporter_id: UUID | None
    labels: list[str]
    due_date: date | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
```

### backend/app/application/validators/__init__.py

```python
"""Application-layer validators."""

from app.application.validators.work_item_validator import WorkItemValidator

__all__ = ["WorkItemValidator"]
```

### backend/app/application/validators/work_item_validator.py

```python
"""Cross-aggregate validators for work item operations."""

from __future__ import annotations

from uuid import UUID

from app.core.exceptions import NotFoundError, ValidationError
from app.domain.entities.user import User
from app.domain.enums import WorkItemType
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class WorkItemValidator:
    """Validates references between work items, projects, sprints, and users."""

    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self._uow = uow

    def ensure_project_belongs_to_org(
        self, project_id: UUID, organization_id: UUID | None
    ) -> None:
        project = self._uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        if organization_id is not None and project.organization_id != organization_id:
            raise ValidationError("Project does not belong to your organization")

    def ensure_sprint_belongs_to_project(
        self, sprint_id: UUID | None, project_id: UUID
    ) -> None:
        if sprint_id is None:
            return
        sprint = self._uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        if sprint.project_id != project_id:
            raise ValidationError("Sprint does not belong to the given project")

    def ensure_assignee_in_org(
        self, assignee_id: UUID | None, organization_id: UUID | None
    ) -> User | None:
        if assignee_id is None:
            return None
        user = self._uow.users.get_by_id(assignee_id)
        if user is None:
            raise NotFoundError(f"User {assignee_id} not found")
        if not user.is_active:
            raise ValidationError("Assignee is not an active user")
        if organization_id is not None and user.organization_id != organization_id:
            raise ValidationError("Assignee does not belong to your organization")
        return user

    def ensure_parent_valid(
        self,
        parent_id: UUID | None,
        project_id: UUID,
        item_type: WorkItemType,
    ) -> None:
        if parent_id is None:
            return
        parent = self._uow.work_items.get_by_id(parent_id)
        if parent is None:
            raise NotFoundError(f"Parent work item {parent_id} not found")
        if parent.project_id != project_id:
            raise ValidationError(
                "Parent work item must belong to the same project"
            )
        if item_type == WorkItemType.EPIC and parent.item_type == WorkItemType.EPIC:
            raise ValidationError("Epics cannot have another epic as parent")

    def ensure_epic_valid(
        self,
        epic_id: UUID | None,
        project_id: UUID,
        item_type: WorkItemType,
    ) -> None:
        if epic_id is None:
            return
        if item_type == WorkItemType.EPIC:
            raise ValidationError("An epic cannot belong to another epic")
        epic = self._uow.work_items.get_by_id(epic_id)
        if epic is None:
            raise NotFoundError(f"Epic {epic_id} not found")
        if epic.item_type != WorkItemType.EPIC:
            raise ValidationError("Referenced item is not an epic")
        if epic.project_id != project_id:
            raise ValidationError("Epic must belong to the same project")
```

### backend/app/application/use_cases/work_items/__init__.py

```python
"""Work item use cases."""

from app.application.use_cases.work_items.assign_work_item import (
    AssignWorkItemCommand,
    AssignWorkItemUseCase,
)
from app.application.use_cases.work_items.change_status import (
    ChangeWorkItemStatusCommand,
    ChangeWorkItemStatusUseCase,
)
from app.application.use_cases.work_items.create_work_item import (
    CreateWorkItemCommand,
    CreateWorkItemUseCase,
)
from app.application.use_cases.work_items.delete_work_item import (
    DeleteWorkItemCommand,
    DeleteWorkItemUseCase,
)
from app.application.use_cases.work_items.get_work_item import (
    GetWorkItemQuery,
    GetWorkItemUseCase,
)
from app.application.use_cases.work_items.list_work_items import (
    ListWorkItemsQuery,
    ListWorkItemsUseCase,
)
from app.application.use_cases.work_items.move_work_item import (
    MoveWorkItemToSprintCommand,
    MoveWorkItemToSprintUseCase,
)
from app.application.use_cases.work_items.update_work_item import (
    UpdateWorkItemCommand,
    UpdateWorkItemUseCase,
)

__all__ = [
    "AssignWorkItemCommand",
    "AssignWorkItemUseCase",
    "ChangeWorkItemStatusCommand",
    "ChangeWorkItemStatusUseCase",
    "CreateWorkItemCommand",
    "CreateWorkItemUseCase",
    "DeleteWorkItemCommand",
    "DeleteWorkItemUseCase",
    "GetWorkItemQuery",
    "GetWorkItemUseCase",
    "ListWorkItemsQuery",
    "ListWorkItemsUseCase",
    "MoveWorkItemToSprintCommand",
    "MoveWorkItemToSprintUseCase",
    "UpdateWorkItemCommand",
    "UpdateWorkItemUseCase",
]
```

### backend/app/application/use_cases/work_items/create_work_item.py

```python
"""Create work item use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import ConflictError
from app.domain.entities.work_item import WorkItem
from app.domain.entities.work_item_extensions import (
    ensure_hierarchy,
    normalize_labels,
)
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.domain.services.permissions import Permission, PermissionRegistry
from app.domain.services.authorization_service import AuthorizationDomainService


@dataclass(frozen=True)
class CreateWorkItemCommand:
    """Create work item command."""

    project_id: UUID
    title: str
    context: RequestContext
    description: str | None = None
    item_type: WorkItemType = WorkItemType.STORY
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    story_points: int | None = None
    estimated_hours: float | None = None
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    assignee_id: UUID | None = None
    external_key: str | None = None
    labels: list[str] = field(default_factory=list)


class CreateWorkItemUseCase(UseCase[CreateWorkItemCommand, WorkItemDTO]):
    """Create a new work item."""

    def execute(self, command: CreateWorkItemCommand) -> WorkItemDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            validator = WorkItemValidator(uow)
            org_id = command.context.organization_id

            validator.ensure_project_belongs_to_org(command.project_id, org_id)
            project = uow.projects.get_by_id(command.project_id)
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id if project else None
            )

            ensure_hierarchy(command.item_type, command.epic_id, command.parent_id)
            validator.ensure_sprint_belongs_to_project(
                command.sprint_id, command.project_id
            )
            validator.ensure_parent_valid(
                command.parent_id, command.project_id, command.item_type
            )
            validator.ensure_epic_valid(
                command.epic_id, command.project_id, command.item_type
            )
            validator.ensure_assignee_in_org(command.assignee_id, org_id)

            if command.external_key:
                existing = uow.work_items.get_by_external_key(
                    command.project_id, command.external_key
                )
                if existing is not None:
                    raise ConflictError(
                        f"External key '{command.external_key}' is already in use"
                    )

            item = WorkItem(
                project_id=command.project_id,
                sprint_id=command.sprint_id,
                parent_id=command.parent_id,
                epic_id=command.epic_id,
                external_key=command.external_key,
                title=command.title,
                description=command.description,
                item_type=command.item_type,
                status=WorkItemStatus.BACKLOG,
                priority=command.priority,
                story_points=command.story_points,
                estimated_hours=command.estimated_hours,
                assignee_id=command.assignee_id,
                reporter_id=command.context.actor_id,
                labels=normalize_labels(command.labels),
            )
            created = uow.work_items.add(item)
            uow.commit()
            return work_item_to_dto(created)
```

### backend/app/application/use_cases/work_items/update_work_item.py

```python
"""Update work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.entities.work_item_extensions import (
    apply_status_change,
    normalize_labels,
)
from app.domain.enums import WorkItemPriority, WorkItemStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateWorkItemCommand:
    """Partial update command for a work item."""

    work_item_id: UUID
    context: RequestContext
    title: str | None = None
    description: str | None = None
    priority: WorkItemPriority | None = None
    status: WorkItemStatus | None = None
    story_points: int | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    sprint_id: UUID | None = None
    parent_id: UUID | None = None
    epic_id: UUID | None = None
    assignee_id: UUID | None = None
    labels: list[str] | None = None
    _sprint_id_provided: bool = False
    _parent_id_provided: bool = False
    _epic_id_provided: bool = False
    _assignee_id_provided: bool = False


class UpdateWorkItemUseCase(UseCase[UpdateWorkItemCommand, WorkItemDTO]):
    """Apply a partial update to a work item."""

    def execute(self, command: UpdateWorkItemCommand) -> WorkItemDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(command.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {command.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id
            )

            validator = WorkItemValidator(uow)
            org_id = project.organization_id

            if command.title is not None:
                if not command.title.strip():
                    raise ValidationError("Title cannot be empty")
                item.title = command.title.strip()
            if command.description is not None:
                item.description = command.description
            if command.priority is not None:
                item.priority = command.priority
            if command.story_points is not None:
                if command.story_points < 0:
                    raise ValidationError("Story points cannot be negative")
                item.story_points = command.story_points
            if command.estimated_hours is not None:
                if command.estimated_hours < 0:
                    raise ValidationError("Estimated hours cannot be negative")
                item.estimated_hours = command.estimated_hours
            if command.actual_hours is not None:
                if command.actual_hours < 0:
                    raise ValidationError("Actual hours cannot be negative")
                item.actual_hours = command.actual_hours
            if command.labels is not None:
                item.labels = normalize_labels(command.labels)

            if command._sprint_id_provided:
                validator.ensure_sprint_belongs_to_project(
                    command.sprint_id, item.project_id
                )
                item.sprint_id = command.sprint_id
            if command._parent_id_provided:
                validator.ensure_parent_valid(
                    command.parent_id, item.project_id, item.item_type
                )
                item.parent_id = command.parent_id
            if command._epic_id_provided:
                validator.ensure_epic_valid(
                    command.epic_id, item.project_id, item.item_type
                )
                item.epic_id = command.epic_id
            if command._assignee_id_provided:
                validator.ensure_assignee_in_org(command.assignee_id, org_id)
                item.assignee_id = command.assignee_id

            item.touch()

            if command.status is not None and command.status != item.status:
                apply_status_change(item, command.status)

            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)
```

### backend/app/application/use_cases/work_items/delete_work_item.py

```python
"""Delete work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.enums import WorkItemStatus, WorkItemType
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class DeleteWorkItemCommand:
    """Delete (soft) a work item."""

    work_item_id: UUID
    context: RequestContext


class DeleteWorkItemUseCase(UseCase[DeleteWorkItemCommand, None]):
    """Soft-delete a work item after checking business rules."""

    def execute(self, command: DeleteWorkItemCommand) -> None:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(command.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {command.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id
            )

            if item.status == WorkItemStatus.DONE:
                raise BusinessRuleViolationError(
                    "Completed work items cannot be deleted; cancel them instead"
                )

            if item.item_type == WorkItemType.EPIC:
                children = uow.work_items.list_by_epic(item.id)
                if children:
                    raise BusinessRuleViolationError(
                        "Cannot delete an epic that still has child work items"
                    )

            uow.work_items.delete(command.work_item_id)
            uow.commit()
```

### backend/app/application/use_cases/work_items/get_work_item.py

```python
"""Get work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class GetWorkItemQuery:
    """Query for a single work item."""

    work_item_id: UUID
    context: RequestContext


class GetWorkItemUseCase(UseCase[GetWorkItemQuery, WorkItemDTO]):
    """Retrieve a work item by ID."""

    def execute(self, query: GetWorkItemQuery) -> WorkItemDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.WORK_ITEM_READ)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(query.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {query.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, project.organization_id
            )
            return work_item_to_dto(item)
```

### backend/app/application/use_cases/work_items/list_work_items.py

```python
"""List work items use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.domain.repositories.specifications import PageRequest, WorkItemFilter
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListWorkItemsQuery:
    """Filter + pagination query for work items."""

    context: RequestContext
    page: PageDTO = field(default_factory=PageDTO)
    project_id: UUID | None = None
    sprint_id: UUID | None = None
    assignee_id: UUID | None = None
    reporter_id: UUID | None = None
    epic_id: UUID | None = None
    item_types: tuple[str, ...] = ()
    statuses: tuple[str, ...] = ()
    priorities: tuple[str, ...] = ()
    labels: tuple[str, ...] = ()
    search: str | None = None
    completed_after: datetime | None = None
    completed_before: datetime | None = None


class ListWorkItemsUseCase(
    UseCase[ListWorkItemsQuery, PaginatedResultDTO[WorkItemDTO]]
):
    """List work items belonging to the caller's organization."""

    def execute(
        self, query: ListWorkItemsQuery
    ) -> PaginatedResultDTO[WorkItemDTO]:
        PermissionRegistry.ensure(query.context.actor, Permission.WORK_ITEM_READ)

        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )
        spec = WorkItemFilter(
            organization_id=query.context.organization_id,
            project_id=query.project_id,
            sprint_id=query.sprint_id,
            assignee_id=query.assignee_id,
            reporter_id=query.reporter_id,
            epic_id=query.epic_id,
            item_types=query.item_types,
            statuses=query.statuses,
            priorities=query.priorities,
            labels=query.labels,
            search=query.search,
            completed_after=query.completed_after,
            completed_before=query.completed_before,
        )

        with self._uow_factory() as uow:
            items = uow.work_items.find(spec, page)
            total = uow.work_items.count(spec)

        return PaginatedResultDTO[WorkItemDTO](
            items=[work_item_to_dto(i) for i in items],
            total=total,
            limit=page.limit,
            offset=page.offset,
        )
```

### backend/app/application/use_cases/work_items/assign_work_item.py

```python
"""Assign work item use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class AssignWorkItemCommand:
    """Assign or unassign a work item."""

    work_item_id: UUID
    assignee_id: UUID | None
    context: RequestContext


class AssignWorkItemUseCase(UseCase[AssignWorkItemCommand, WorkItemDTO]):
    """Reassign a work item to a user (or unassign)."""

    def execute(self, command: AssignWorkItemCommand) -> WorkItemDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(command.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {command.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id
            )

            validator = WorkItemValidator(uow)
            validator.ensure_assignee_in_org(
                command.assignee_id, project.organization_id
            )

            item.reassign(command.assignee_id)
            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)
```

### backend/app/application/use_cases/work_items/move_work_item.py

```python
"""Move work item to a sprint (or backlog)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.work_item_validator import WorkItemValidator
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.enums import WorkItemStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class MoveWorkItemToSprintCommand:
    """Move a work item to a sprint or back to the backlog."""

    work_item_id: UUID
    sprint_id: UUID | None
    context: RequestContext


class MoveWorkItemToSprintUseCase(
    UseCase[MoveWorkItemToSprintCommand, WorkItemDTO]
):
    """Move a work item to a target sprint (or unassign it from any sprint)."""

    def execute(self, command: MoveWorkItemToSprintCommand) -> WorkItemDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(command.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {command.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id
            )

            if item.status == WorkItemStatus.DONE:
                raise BusinessRuleViolationError(
                    "Cannot move a completed work item between sprints"
                )

            validator = WorkItemValidator(uow)
            validator.ensure_sprint_belongs_to_project(
                command.sprint_id, item.project_id
            )

            if command.sprint_id is None:
                item.remove_from_sprint()
            else:
                item.assign_to_sprint(command.sprint_id)

            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)
```

### backend/app/application/use_cases/work_items/change_status.py

```python
"""Change work item status use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.work_item import WorkItemDTO
from app.application.mappers import work_item_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.entities.work_item_extensions import apply_status_change
from app.domain.enums import WorkItemStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ChangeWorkItemStatusCommand:
    """Change the status of a work item."""

    work_item_id: UUID
    target_status: WorkItemStatus
    context: RequestContext
    actual_hours: float | None = None


class ChangeWorkItemStatusUseCase(
    UseCase[ChangeWorkItemStatusCommand, WorkItemDTO]
):
    """Apply a validated status transition to a work item."""

    def execute(self, command: ChangeWorkItemStatusCommand) -> WorkItemDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.WORK_ITEM_WRITE)

        with self._uow_factory() as uow:
            item = uow.work_items.get_by_id(command.work_item_id)
            if item is None:
                raise NotFoundError(f"Work item {command.work_item_id} not found")

            project = uow.projects.get_by_id(item.project_id)
            if project is None:
                raise NotFoundError("Work item's project not found")
            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, project.organization_id
            )

            if (
                command.target_status == WorkItemStatus.DONE
                and command.actual_hours is not None
            ):
                if command.actual_hours < 0:
                    raise ValidationError("Actual hours cannot be negative")
                item.actual_hours = command.actual_hours

            apply_status_change(item, command.target_status)
            updated = uow.work_items.update(item)
            uow.commit()
            return work_item_to_dto(updated)
```

### backend/app/api/routers/work_items.py

```python
"""Work item endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.work_item import (
    WorkItemCreateDTO,
    WorkItemDTO,
    WorkItemUpdateDTO,
)
from app.application.dtos.work_item_extensions import (
    WorkItemAssignDTO,
    WorkItemMoveDTO,
    WorkItemReplaceDTO,
    WorkItemStatusChangeDTO,
)
from app.application.use_cases.work_items import (
    AssignWorkItemCommand,
    AssignWorkItemUseCase,
    ChangeWorkItemStatusCommand,
    ChangeWorkItemStatusUseCase,
    CreateWorkItemCommand,
    CreateWorkItemUseCase,
    DeleteWorkItemCommand,
    DeleteWorkItemUseCase,
    GetWorkItemQuery,
    GetWorkItemUseCase,
    ListWorkItemsQuery,
    ListWorkItemsUseCase,
    MoveWorkItemToSprintCommand,
    MoveWorkItemToSprintUseCase,
    UpdateWorkItemCommand,
    UpdateWorkItemUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/work-items", tags=["work-items"])


@router.post(
    "",
    response_model=WorkItemDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a work item",
)
def create_work_item(
    payload: WorkItemCreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Create a new work item."""
    use_case = CreateWorkItemUseCase()
    return use_case.execute(
        CreateWorkItemCommand(
            project_id=payload.project_id,
            title=payload.title,
            description=payload.description,
            item_type=payload.item_type,
            priority=payload.priority,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            external_key=payload.external_key,
            labels=list(payload.labels),
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[WorkItemDTO],
    status_code=status.HTTP_200_OK,
    summary="List work items",
)
def list_work_items(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    project_id: UUID | None = Query(default=None),
    sprint_id: UUID | None = Query(default=None),
    assignee_id: UUID | None = Query(default=None),
    reporter_id: UUID | None = Query(default=None),
    epic_id: UUID | None = Query(default=None),
    item_type: list[WorkItemType] | None = Query(default=None),
    status_filter: list[WorkItemStatus] | None = Query(default=None, alias="status"),
    priority: list[WorkItemPriority] | None = Query(default=None),
    label: list[str] | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
    completed_after: datetime | None = Query(default=None),
    completed_before: datetime | None = Query(default=None),
) -> PaginatedResultDTO[WorkItemDTO]:
    """List work items with filtering."""
    use_case = ListWorkItemsUseCase()
    return use_case.execute(
        ListWorkItemsQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            project_id=project_id,
            sprint_id=sprint_id,
            assignee_id=assignee_id,
            reporter_id=reporter_id,
            epic_id=epic_id,
            item_types=tuple(t.value for t in item_type) if item_type else (),
            statuses=tuple(s.value for s in status_filter) if status_filter else (),
            priorities=tuple(p.value for p in priority) if priority else (),
            labels=tuple(label) if label else (),
            search=search,
            completed_after=completed_after,
            completed_before=completed_before,
        )
    )


@router.get(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a work item",
)
def get_work_item(
    work_item_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_READ))],
) -> WorkItemDTO:
    """Retrieve a work item by ID."""
    use_case = GetWorkItemUseCase()
    return use_case.execute(
        GetWorkItemQuery(work_item_id=work_item_id, context=context)
    )


@router.patch(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a work item",
)
def patch_work_item(
    work_item_id: UUID,
    payload: WorkItemUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Partially update a work item."""
    provided = payload.model_fields_set
    use_case = UpdateWorkItemUseCase()
    return use_case.execute(
        UpdateWorkItemCommand(
            work_item_id=work_item_id,
            context=context,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            actual_hours=payload.actual_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            labels=payload.labels,
            _sprint_id_provided="sprint_id" in provided,
            _parent_id_provided="parent_id" in provided,
            _epic_id_provided="epic_id" in provided,
            _assignee_id_provided="assignee_id" in provided,
        )
    )


@router.put(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a work item (full update)",
)
def replace_work_item(
    work_item_id: UUID,
    payload: WorkItemReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Full-replacement update of a work item."""
    use_case = UpdateWorkItemUseCase()
    return use_case.execute(
        UpdateWorkItemCommand(
            work_item_id=work_item_id,
            context=context,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            actual_hours=payload.actual_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            labels=payload.labels,
            _sprint_id_provided=True,
            _parent_id_provided=True,
            _epic_id_provided=True,
            _assignee_id_provided=True,
        )
    )


@router.delete(
    "/{work_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a work item",
)
def delete_work_item(
    work_item_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> None:
    """Soft-delete a work item."""
    use_case = DeleteWorkItemUseCase()
    use_case.execute(
        DeleteWorkItemCommand(work_item_id=work_item_id, context=context)
    )


@router.patch(
    "/{work_item_id}/assign",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Assign or unassign a work item",
)
def assign_work_item(
    work_item_id: UUID,
    payload: WorkItemAssignDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Reassign a work item to a user."""
    use_case = AssignWorkItemUseCase()
    return use_case.execute(
        AssignWorkItemCommand(
            work_item_id=work_item_id,
            assignee_id=payload.assignee_id,
            context=context,
        )
    )


@router.patch(
    "/{work_item_id}/status",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Change a work item's status",
)
def change_work_item_status(
    work_item_id: UUID,
    payload: WorkItemStatusChangeDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Change the status of a work item."""
    use_case = ChangeWorkItemStatusUseCase()
    return use_case.execute(
        ChangeWorkItemStatusCommand(
            work_item_id=work_item_id,
            target_status=payload.status,
            actual_hours=payload.actual_hours,
            context=context,
        )
    )


@router.patch(
    "/{work_item_id}/move",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Move a work item to a sprint or the backlog",
)
def move_work_item(
    work_item_id: UUID,
    payload: WorkItemMoveDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Move a work item into a sprint or return it to the backlog."""
    use_case = MoveWorkItemToSprintUseCase()
    return use_case.execute(
        MoveWorkItemToSprintCommand(
            work_item_id=work_item_id,
            sprint_id=payload.sprint_id,
            context=context,
        )
    )
```

================================================================================

### backend/app/domain/entities/business_outcome_extensions.py

```python
"""Extension helpers for the BusinessOutcome aggregate.

These helpers centralize lifecycle rules (activation, archival, deletion
guards) used by the outcome use cases without modifying the existing
`BusinessOutcome` entity module.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Final

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.enums import OutcomeStatus

_TERMINAL_STATES: Final[frozenset[OutcomeStatus]] = frozenset(
    {OutcomeStatus.ACHIEVED, OutcomeStatus.ABANDONED}
)

_LIVE_STATES: Final[frozenset[OutcomeStatus]] = frozenset(
    {
        OutcomeStatus.PROPOSED,
        OutcomeStatus.ACTIVE,
        OutcomeStatus.AT_RISK,
        OutcomeStatus.OFF_TRACK,
    }
)


class OutcomeLifecycle:
    """Encapsulates lifecycle predicates for a business outcome."""

    @staticmethod
    def is_archived(outcome: BusinessOutcome) -> bool:
        """Return True when the outcome has been archived (abandoned)."""
        return outcome.status == OutcomeStatus.ABANDONED

    @staticmethod
    def is_terminal(outcome: BusinessOutcome) -> bool:
        """Return True when the outcome is in a terminal state."""
        return outcome.status in _TERMINAL_STATES

    @staticmethod
    def is_live(outcome: BusinessOutcome) -> bool:
        """Return True when the outcome is actively tracked."""
        return outcome.status in _LIVE_STATES

    @staticmethod
    def ensure_editable(outcome: BusinessOutcome) -> None:
        """Ensure the outcome may still be edited."""
        if OutcomeLifecycle.is_archived(outcome):
            raise BusinessRuleViolationError(
                "Archived business outcomes are read-only"
            )

    @staticmethod
    def ensure_status_change_allowed(
        outcome: BusinessOutcome, target: OutcomeStatus
    ) -> None:
        """Validate an explicit status change against lifecycle rules."""
        if outcome.status == target:
            raise BusinessRuleViolationError(
                f"Outcome is already in status '{target.value}'"
            )
        if OutcomeLifecycle.is_archived(outcome):
            raise BusinessRuleViolationError(
                "Archived outcomes cannot change status"
            )
        if (
            outcome.status == OutcomeStatus.ACHIEVED
            and target != OutcomeStatus.ACTIVE
        ):
            raise BusinessRuleViolationError(
                "Achieved outcomes can only be reopened as 'active'"
            )


def apply_status_change(outcome: BusinessOutcome, target: OutcomeStatus) -> None:
    """Apply a validated lifecycle transition."""
    OutcomeLifecycle.ensure_status_change_allowed(outcome, target)
    if target == OutcomeStatus.ACTIVE:
        outcome.status = OutcomeStatus.ACTIVE
    elif target == OutcomeStatus.AT_RISK:
        outcome.mark_at_risk()
    elif target == OutcomeStatus.OFF_TRACK:
        outcome.mark_off_track()
    elif target == OutcomeStatus.ACHIEVED:
        outcome.achieve()
    elif target == OutcomeStatus.ABANDONED:
        outcome.abandon()
    else:
        outcome.status = target
    outcome.touch()


def validate_value_bounds(
    baseline: Decimal | None,
    target: Decimal | None,
    current: Decimal | None,
) -> None:
    """Validate the coherence of baseline/target/current values."""
    if baseline is None and target is None and current is None:
        return
    if baseline is not None and target is not None and baseline == target:
        # Zero-span is allowed but must be intentional; enforce that current
        # cannot then contradict the goal.
        if current is not None and current < baseline:
            raise ValidationError(
                "Current value cannot be below baseline when baseline equals target"
            )


def validate_target_date(target_date: date | None, today: date | None = None) -> None:
    """Ensure a target date is not absurdly far in the past."""
    if target_date is None:
        return
    reference = today or date.today()
    # Allow historical values (e.g., importing historic outcomes) but bound the
    # window to a decade to catch obvious data errors.
    if (reference - target_date).days > 3650:
        raise ValidationError("target_date is more than 10 years in the past")
```

### backend/app/application/validators/business_outcome_validator.py

```python
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
```

### backend/app/application/dtos/business_outcome_extensions.py

```python
"""Extended DTOs for business outcome operations."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.application.dtos.kpi import KPIDTO
from app.application.dtos.work_item import WorkItemDTO
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.domain.enums import OutcomeStatus


class BusinessOutcomeReplaceDTO(BaseModel):
    """Full-replacement (PUT) payload for a business outcome."""

    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    hypothesis: str | None = Field(default=None, max_length=4000)
    status: OutcomeStatus
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = Field(default=None, ge=0, le=100)
    financial_impact_estimate: Decimal | None = None


class BusinessOutcomeArchiveDTO(BaseModel):
    """Payload for archiving/unarchiving a business outcome."""

    archived: bool = True


class BusinessOutcomeDetailDTO(BaseModel):
    """Aggregated read model for a business outcome with linked children."""

    model_config = ConfigDict(from_attributes=True)

    outcome: BusinessOutcomeDTO
    kpis: list[KPIDTO]
    linked_work_items: list[WorkItemDTO]
    attribution_count: int
    latest_snapshot_at: datetime | None = None
```

### backend/app/application/use_cases/outcomes/__init__.py

```python
"""Business outcome use cases."""

from app.application.use_cases.outcomes.archive_outcome import (
    ArchiveBusinessOutcomeCommand,
    ArchiveBusinessOutcomeUseCase,
)
from app.application.use_cases.outcomes.create_outcome import (
    CreateBusinessOutcomeCommand,
    CreateBusinessOutcomeUseCase,
)
from app.application.use_cases.outcomes.delete_outcome import (
    DeleteBusinessOutcomeCommand,
    DeleteBusinessOutcomeUseCase,
)
from app.application.use_cases.outcomes.get_outcome import (
    GetBusinessOutcomeQuery,
    GetBusinessOutcomeUseCase,
)
from app.application.use_cases.outcomes.list_outcomes import (
    ListBusinessOutcomesQuery,
    ListBusinessOutcomesUseCase,
)
from app.application.use_cases.outcomes.update_outcome import (
    UpdateBusinessOutcomeCommand,
    UpdateBusinessOutcomeUseCase,
)

__all__ = [
    "ArchiveBusinessOutcomeCommand",
    "ArchiveBusinessOutcomeUseCase",
    "CreateBusinessOutcomeCommand",
    "CreateBusinessOutcomeUseCase",
    "DeleteBusinessOutcomeCommand",
    "DeleteBusinessOutcomeUseCase",
    "GetBusinessOutcomeQuery",
    "GetBusinessOutcomeUseCase",
    "ListBusinessOutcomesQuery",
    "ListBusinessOutcomesUseCase",
    "UpdateBusinessOutcomeCommand",
    "UpdateBusinessOutcomeUseCase",
]
```

### backend/app/application/use_cases/outcomes/create_outcome.py

```python
"""Create business outcome use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.mappers import outcome_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.business_outcome_validator import (
    BusinessOutcomeValidator,
)
from app.core.exceptions import ConflictError
from app.domain.entities.business_outcome import BusinessOutcome
from app.domain.entities.business_outcome_extensions import (
    validate_target_date,
    validate_value_bounds,
)
from app.domain.enums import OutcomeStatus
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class CreateBusinessOutcomeCommand:
    """Create business outcome command."""

    name: str
    context: RequestContext
    owner_id: UUID | None = None
    description: str | None = None
    hypothesis: str | None = None
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = None
    financial_impact_estimate: Decimal | None = None


class CreateBusinessOutcomeUseCase(
    UseCase[CreateBusinessOutcomeCommand, BusinessOutcomeDTO]
):
    """Create a business outcome scoped to the caller's organization."""

    def execute(
        self, command: CreateBusinessOutcomeCommand
    ) -> BusinessOutcomeDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        org_id = command.context.organization_id
        if org_id is None:
            raise ConflictError(
                "Outcomes can only be created within an organization context"
            )

        validate_target_date(command.target_date)
        validate_value_bounds(
            command.baseline_value, command.target_value, command.current_value
        )

        with self._uow_factory() as uow:
            validator = BusinessOutcomeValidator(uow)
            validator.ensure_unique_name(org_id, command.name)
            validator.ensure_owner_in_org(command.owner_id, org_id)

            outcome = BusinessOutcome(
                organization_id=org_id,
                owner_id=command.owner_id,
                name=command.name.strip(),
                description=command.description,
                hypothesis=command.hypothesis,
                status=OutcomeStatus.PROPOSED,
                target_date=command.target_date,
                baseline_value=command.baseline_value,
                target_value=command.target_value,
                current_value=command.current_value,
                confidence_score=command.confidence_score,
                financial_impact_estimate=command.financial_impact_estimate,
            )
            created = uow.outcomes.add(outcome)
            uow.commit()
            return outcome_to_dto(created)
```

### backend/app/application/use_cases/outcomes/update_outcome.py

```python
"""Update business outcome use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.mappers import outcome_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.business_outcome_validator import (
    BusinessOutcomeValidator,
)
from app.core.exceptions import NotFoundError
from app.domain.entities.business_outcome_extensions import (
    OutcomeLifecycle,
    apply_status_change,
    validate_target_date,
    validate_value_bounds,
)
from app.domain.enums import OutcomeStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateBusinessOutcomeCommand:
    """Update business outcome command."""

    outcome_id: UUID
    context: RequestContext
    name: str | None = None
    description: str | None = None
    hypothesis: str | None = None
    owner_id: UUID | None = None
    status: OutcomeStatus | None = None
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = None
    financial_impact_estimate: Decimal | None = None
    _name_provided: bool = False
    _description_provided: bool = False
    _hypothesis_provided: bool = False
    _owner_provided: bool = False
    _target_date_provided: bool = False
    _baseline_value_provided: bool = False
    _target_value_provided: bool = False
    _current_value_provided: bool = False
    _confidence_score_provided: bool = False
    _financial_impact_provided: bool = False


class UpdateBusinessOutcomeUseCase(
    UseCase[UpdateBusinessOutcomeCommand, BusinessOutcomeDTO]
):
    """Update a business outcome."""

    def execute(
        self, command: UpdateBusinessOutcomeCommand
    ) -> BusinessOutcomeDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(command.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {command.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, outcome.organization_id
            )
            OutcomeLifecycle.ensure_editable(outcome)

            validator = BusinessOutcomeValidator(uow)

            if command._name_provided and command.name is not None:
                validator.ensure_unique_name(
                    outcome.organization_id, command.name, exclude_id=outcome.id
                )
                outcome.name = command.name.strip()

            if command._description_provided:
                outcome.description = command.description
            if command._hypothesis_provided:
                outcome.hypothesis = command.hypothesis

            if command._owner_provided:
                validator.ensure_owner_in_org(command.owner_id, outcome.organization_id)
                outcome.owner_id = command.owner_id

            if command._target_date_provided:
                validate_target_date(command.target_date)
                outcome.target_date = command.target_date

            new_baseline = (
                command.baseline_value
                if command._baseline_value_provided
                else outcome.baseline_value
            )
            new_target = (
                command.target_value
                if command._target_value_provided
                else outcome.target_value
            )
            new_current = (
                command.current_value
                if command._current_value_provided
                else outcome.current_value
            )
            validate_value_bounds(new_baseline, new_target, new_current)

            if command._baseline_value_provided:
                outcome.baseline_value = command.baseline_value
            if command._target_value_provided:
                outcome.target_value = command.target_value
            if command._current_value_provided:
                outcome.current_value = command.current_value
            if command._confidence_score_provided:
                outcome.confidence_score = command.confidence_score
            if command._financial_impact_provided:
                outcome.financial_impact_estimate = command.financial_impact_estimate

            outcome.touch()

            if command.status is not None and command.status != outcome.status:
                apply_status_change(outcome, command.status)

            updated = uow.outcomes.update(outcome)
            uow.commit()
            return outcome_to_dto(updated)
```

### backend/app/application/use_cases/outcomes/delete_outcome.py

```python
"""Delete business outcome use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.use_cases.base import UseCase
from app.application.validators.business_outcome_validator import (
    BusinessOutcomeValidator,
)
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class DeleteBusinessOutcomeCommand:
    """Soft-delete a business outcome."""

    outcome_id: UUID
    context: RequestContext


class DeleteBusinessOutcomeUseCase(UseCase[DeleteBusinessOutcomeCommand, None]):
    """Delete a business outcome after enforcing business rules."""

    def execute(self, command: DeleteBusinessOutcomeCommand) -> None:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(command.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {command.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, outcome.organization_id
            )

            attributions = uow.attributions.list_by_outcome(outcome.id)
            if attributions:
                raise BusinessRuleViolationError(
                    "Cannot delete an outcome that has attributions; archive it instead"
                )

            BusinessOutcomeValidator(uow).ensure_deletable(outcome.id)

            # Detach any linked KPIs so they remain usable at the organization level.
            for kpi in uow.kpis.list_by_outcome(outcome.id):
                kpi.outcome_id = None
                kpi.touch()
                uow.kpis.update(kpi)

            uow.outcomes.delete(outcome.id)
            uow.commit()
```

### backend/app/application/use_cases/outcomes/get_outcome.py

```python
"""Get business outcome use case (with linked children)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.business_outcome_extensions import (
    BusinessOutcomeDetailDTO,
)
from app.application.mappers import (
    kpi_to_dto,
    outcome_to_dto,
    work_item_to_dto,
)
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class GetBusinessOutcomeQuery:
    """Query for a single business outcome."""

    outcome_id: UUID
    context: RequestContext
    include_linked: bool = True


class GetBusinessOutcomeUseCase(
    UseCase[GetBusinessOutcomeQuery, BusinessOutcomeDetailDTO]
):
    """Retrieve a business outcome and its linked children."""

    def execute(
        self, query: GetBusinessOutcomeQuery
    ) -> BusinessOutcomeDetailDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.OUTCOME_READ)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(query.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {query.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, outcome.organization_id
            )

            kpis = []
            work_items = []
            attribution_count = 0
            latest_snapshot_at = None

            if query.include_linked:
                kpi_entities = uow.kpis.list_by_outcome(outcome.id)
                kpis = [kpi_to_dto(k) for k in kpi_entities]

                attributions = uow.attributions.list_by_outcome(outcome.id)
                attribution_count = len(attributions)

                seen_ids: set[UUID] = set()
                for attribution in attributions:
                    if attribution.work_item_id is None:
                        continue
                    if attribution.work_item_id in seen_ids:
                        continue
                    seen_ids.add(attribution.work_item_id)
                    item = uow.work_items.get_by_id(attribution.work_item_id)
                    if item is not None:
                        work_items.append(work_item_to_dto(item))

                for kpi in kpi_entities:
                    snapshot = uow.metric_snapshots.latest_for_kpi(kpi.id)
                    if snapshot is None:
                        continue
                    if (
                        latest_snapshot_at is None
                        or snapshot.recorded_at > latest_snapshot_at
                    ):
                        latest_snapshot_at = snapshot.recorded_at

            return BusinessOutcomeDetailDTO(
                outcome=outcome_to_dto(outcome),
                kpis=kpis,
                linked_work_items=work_items,
                attribution_count=attribution_count,
                latest_snapshot_at=latest_snapshot_at,
            )
```

### backend/app/application/use_cases/outcomes/list_outcomes.py

```python
"""List business outcomes use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.mappers import outcome_to_dto
from app.application.use_cases.base import UseCase
from app.domain.repositories.specifications import OutcomeFilter, PageRequest
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListBusinessOutcomesQuery:
    """Filter + pagination query for business outcomes."""

    context: RequestContext
    page: PageDTO = field(default_factory=PageDTO)
    owner_id: UUID | None = None
    statuses: tuple[str, ...] = ()
    target_before: date | None = None
    target_after: date | None = None
    search: str | None = None


class ListBusinessOutcomesUseCase(
    UseCase[ListBusinessOutcomesQuery, PaginatedResultDTO[BusinessOutcomeDTO]]
):
    """List business outcomes for the caller's organization."""

    def execute(
        self, query: ListBusinessOutcomesQuery
    ) -> PaginatedResultDTO[BusinessOutcomeDTO]:
        PermissionRegistry.ensure(query.context.actor, Permission.OUTCOME_READ)

        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )
        spec = OutcomeFilter(
            organization_id=query.context.organization_id,
            owner_id=query.owner_id,
            statuses=query.statuses,
            target_before=query.target_before,
            target_after=query.target_after,
            search=query.search,
        )

        with self._uow_factory() as uow:
            items = uow.outcomes.find(spec, page)
            total = uow.outcomes.count(spec)

        return PaginatedResultDTO[BusinessOutcomeDTO](
            items=[outcome_to_dto(o) for o in items],
            total=total,
            limit=page.limit,
            offset=page.offset,
        )
```

### backend/app/application/use_cases/outcomes/archive_outcome.py

```python
"""Archive (or restore) a business outcome."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.mappers import outcome_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.enums import OutcomeStatus
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ArchiveBusinessOutcomeCommand:
    """Archive or restore a business outcome."""

    outcome_id: UUID
    context: RequestContext
    archived: bool = True


class ArchiveBusinessOutcomeUseCase(
    UseCase[ArchiveBusinessOutcomeCommand, BusinessOutcomeDTO]
):
    """Archive a business outcome (transition to ABANDONED) or restore it."""

    def execute(
        self, command: ArchiveBusinessOutcomeCommand
    ) -> BusinessOutcomeDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.OUTCOME_MANAGE)

        with self._uow_factory() as uow:
            outcome = uow.outcomes.get_by_id(command.outcome_id)
            if outcome is None:
                raise NotFoundError(f"Outcome {command.outcome_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, outcome.organization_id
            )

            if command.archived:
                if outcome.status == OutcomeStatus.ABANDONED:
                    raise BusinessRuleViolationError(
                        "Outcome is already archived"
                    )
                if outcome.status == OutcomeStatus.ACHIEVED:
                    raise BusinessRuleViolationError(
                        "Achieved outcomes cannot be archived; keep them for reporting"
                    )
                outcome.abandon()
            else:
                if outcome.status != OutcomeStatus.ABANDONED:
                    raise BusinessRuleViolationError(
                        "Only archived outcomes can be restored"
                    )
                outcome.status = OutcomeStatus.PROPOSED
                outcome.touch()

            updated = uow.outcomes.update(outcome)
            uow.commit()
            return outcome_to_dto(updated)
```

### backend/app/api/routers/business_outcomes.py

```python
"""Business outcome endpoints."""

from __future__ import annotations

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.business_outcome_extensions import (
    BusinessOutcomeArchiveDTO,
    BusinessOutcomeDetailDTO,
    BusinessOutcomeReplaceDTO,
)
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.outcome import (
    BusinessOutcomeCreateDTO,
    BusinessOutcomeDTO,
    BusinessOutcomeUpdateDTO,
)
from app.application.use_cases.outcomes import (
    ArchiveBusinessOutcomeCommand,
    ArchiveBusinessOutcomeUseCase,
    CreateBusinessOutcomeCommand,
    CreateBusinessOutcomeUseCase,
    DeleteBusinessOutcomeCommand,
    DeleteBusinessOutcomeUseCase,
    GetBusinessOutcomeQuery,
    GetBusinessOutcomeUseCase,
    ListBusinessOutcomesQuery,
    ListBusinessOutcomesUseCase,
    UpdateBusinessOutcomeCommand,
    UpdateBusinessOutcomeUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import OutcomeStatus
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/business-outcomes", tags=["business-outcomes"])


@router.post(
    "",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a business outcome",
)
def create_outcome(
    payload: BusinessOutcomeCreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Create a business outcome."""
    use_case = CreateBusinessOutcomeUseCase()
    return use_case.execute(
        CreateBusinessOutcomeCommand(
            name=payload.name,
            owner_id=payload.owner_id,
            description=payload.description,
            hypothesis=payload.hypothesis,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[BusinessOutcomeDTO],
    status_code=status.HTTP_200_OK,
    summary="List business outcomes",
)
def list_outcomes(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    owner_id: UUID | None = Query(default=None),
    status_filter: list[OutcomeStatus] | None = Query(default=None, alias="status"),
    target_before: date | None = Query(default=None),
    target_after: date | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
) -> PaginatedResultDTO[BusinessOutcomeDTO]:
    """List business outcomes with filtering."""
    use_case = ListBusinessOutcomesUseCase()
    return use_case.execute(
        ListBusinessOutcomesQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            owner_id=owner_id,
            statuses=tuple(s.value for s in status_filter) if status_filter else (),
            target_before=target_before,
            target_after=target_after,
            search=search,
        )
    )


@router.get(
    "/{outcome_id}",
    response_model=BusinessOutcomeDetailDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a business outcome (with linked KPIs and work items)",
)
def get_outcome(
    outcome_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_READ))],
    include_linked: bool = Query(default=True),
) -> BusinessOutcomeDetailDTO:
    """Retrieve a business outcome by ID."""
    use_case = GetBusinessOutcomeUseCase()
    return use_case.execute(
        GetBusinessOutcomeQuery(
            outcome_id=outcome_id,
            context=context,
            include_linked=include_linked,
        )
    )


@router.patch(
    "/{outcome_id}",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a business outcome",
)
def patch_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Partially update a business outcome."""
    provided = payload.model_fields_set
    use_case = UpdateBusinessOutcomeUseCase()
    return use_case.execute(
        UpdateBusinessOutcomeCommand(
            outcome_id=outcome_id,
            context=context,
            name=payload.name,
            description=payload.description,
            hypothesis=payload.hypothesis,
            owner_id=payload.owner_id,
            status=payload.status,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            _name_provided="name" in provided,
            _description_provided="description" in provided,
            _hypothesis_provided="hypothesis" in provided,
            _owner_provided="owner_id" in provided,
            _target_date_provided="target_date" in provided,
            _baseline_value_provided="baseline_value" in provided,
            _target_value_provided="target_value" in provided,
            _current_value_provided="current_value" in provided,
            _confidence_score_provided="confidence_score" in provided,
            _financial_impact_provided="financial_impact_estimate" in provided,
        )
    )


@router.put(
    "/{outcome_id}",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a business outcome (full update)",
)
def replace_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Full-replacement update of a business outcome."""
    use_case = UpdateBusinessOutcomeUseCase()
    return use_case.execute(
        UpdateBusinessOutcomeCommand(
            outcome_id=outcome_id,
            context=context,
            name=payload.name,
            description=payload.description,
            hypothesis=payload.hypothesis,
            owner_id=payload.owner_id,
            status=payload.status,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            _name_provided=True,
            _description_provided=True,
            _hypothesis_provided=True,
            _owner_provided=True,
            _target_date_provided=True,
            _baseline_value_provided=True,
            _target_value_provided=True,
            _current_value_provided=True,
            _confidence_score_provided=True,
            _financial_impact_provided=True,
        )
    )


@router.delete(
    "/{outcome_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a business outcome",
)
def delete_outcome(
    outcome_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> None:
    """Soft-delete a business outcome."""
    use_case = DeleteBusinessOutcomeUseCase()
    use_case.execute(
        DeleteBusinessOutcomeCommand(outcome_id=outcome_id, context=context)
    )


@router.patch(
    "/{outcome_id}/archive",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Archive or restore a business outcome",
)
def archive_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeArchiveDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Archive or restore a business outcome."""
    use_case = ArchiveBusinessOutcomeUseCase()
    return use_case.execute(
        ArchiveBusinessOutcomeCommand(
            outcome_id=outcome_id, archived=payload.archived, context=context
        )
    )
```

================================================================================

### backend/app/domain/entities/kpi_extensions.py

```python
"""Extension helpers for the KPI aggregate.

These helpers centralize lifecycle predicates and value-change rules used by
the KPI use cases, without modifying the existing `KPI` entity module.
"""

from __future__ import annotations

from decimal import Decimal

from app.core.exceptions import BusinessRuleViolationError, ValidationError
from app.domain.entities.kpi import KPI


class KPILifecycle:
    """Lifecycle predicates for a KPI."""

    @staticmethod
    def is_active(kpi: KPI) -> bool:
        return kpi.is_active and not kpi.is_deleted

    @staticmethod
    def has_activation_baseline(kpi: KPI) -> bool:
        """Return True when the KPI has been "activated" (baseline is set)."""
        return kpi.baseline_value is not None

    @staticmethod
    def ensure_editable(kpi: KPI) -> None:
        """Ensure the KPI may still be edited (not soft-deleted)."""
        if kpi.is_deleted:
            raise BusinessRuleViolationError("KPI has been deleted")


def ensure_baseline_stable(kpi: KPI, new_baseline: Decimal | None) -> None:
    """Baseline value cannot change after KPI activation."""
    if new_baseline is None:
        return
    if kpi.baseline_value is None:
        return
    if new_baseline != kpi.baseline_value:
        raise BusinessRuleViolationError(
            "Baseline value cannot be changed after KPI activation"
        )


def ensure_target_direction_consistent(
    baseline: Decimal | None, target: Decimal | None, direction: str
) -> None:
    """Validate that target is consistent with the desired direction."""
    if baseline is None or target is None:
        return
    if direction == "increase" and target < baseline:
        raise ValidationError(
            "Target must be greater than or equal to baseline for INCREASE direction"
        )
    if direction == "decrease" and target > baseline:
        raise ValidationError(
            "Target must be less than or equal to baseline for DECREASE direction"
        )


def ensure_currency_matches_unit(unit: str, currency: str | None) -> None:
    """Ensure currency is provided when unit is monetary and omitted otherwise."""
    if unit == "currency" and not currency:
        raise ValidationError("Currency is required for currency-typed KPIs")
    if unit != "currency" and currency:
        raise ValidationError("Currency should only be set for currency-typed KPIs")
```

### backend/app/application/validators/kpi_validator.py

```python
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
```

### backend/app/application/dtos/kpi_extensions.py

```python
"""Extended DTOs for KPI operations."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.application.dtos.kpi import KPIDTO, MetricSnapshotDTO
from app.domain.enums import KPIDirection, KPIUnit


class KPIReplaceDTO(BaseModel):
    """Full-replacement (PUT) payload for a KPI."""

    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    unit: KPIUnit
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    direction: KPIDirection
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = Field(default=None, max_length=500)
    refresh_frequency_hours: int | None = Field(default=None, ge=1, le=8760)
    is_active: bool = True


class KPITargetUpdateDTO(BaseModel):
    """Payload for updating a KPI's target value."""

    target_value: Decimal
    reason: str | None = Field(default=None, max_length=1000)


class KPIRecordSnapshotDTO(BaseModel):
    """Payload for recording a KPI snapshot from the API layer."""

    value: Decimal
    recorded_at: datetime | None = None
    source: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)


class KPIHistoryDTO(BaseModel):
    """Aggregated read model for a KPI's snapshot history."""

    model_config = ConfigDict(from_attributes=True)

    kpi: KPIDTO
    snapshots: list[MetricSnapshotDTO]
    count: int
    earliest_at: datetime | None = None
    latest_at: datetime | None = None
```

### backend/app/application/use_cases/kpis/__init__.py

```python
"""KPI use cases."""

from app.application.use_cases.kpis.create_kpi import (
    CreateKPICommand,
    CreateKPIUseCase,
)
from app.application.use_cases.kpis.delete_kpi import (
    DeleteKPICommand,
    DeleteKPIUseCase,
)
from app.application.use_cases.kpis.get_kpi import GetKPIQuery, GetKPIUseCase
from app.application.use_cases.kpis.list_history import (
    ListKPIHistoryQuery,
    ListKPIHistoryUseCase,
)
from app.application.use_cases.kpis.list_kpis import (
    ListKPIsQuery,
    ListKPIsUseCase,
)
from app.application.use_cases.kpis.record_snapshot import (
    RecordKPISnapshotCommand,
    RecordKPISnapshotUseCase,
)
from app.application.use_cases.kpis.update_kpi import (
    UpdateKPICommand,
    UpdateKPIUseCase,
)
from app.application.use_cases.kpis.update_target import (
    UpdateKPITargetCommand,
    UpdateKPITargetUseCase,
)

__all__ = [
    "CreateKPICommand",
    "CreateKPIUseCase",
    "DeleteKPICommand",
    "DeleteKPIUseCase",
    "GetKPIQuery",
    "GetKPIUseCase",
    "ListKPIHistoryQuery",
    "ListKPIHistoryUseCase",
    "ListKPIsQuery",
    "ListKPIsUseCase",
    "RecordKPISnapshotCommand",
    "RecordKPISnapshotUseCase",
    "UpdateKPICommand",
    "UpdateKPIUseCase",
    "UpdateKPITargetCommand",
    "UpdateKPITargetUseCase",
]
```

### backend/app/application/use_cases/kpis/create_kpi.py

```python
"""Create KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.kpi_validator import KPIValidator
from app.core.exceptions import ConflictError
from app.domain.entities.kpi import KPI
from app.domain.entities.kpi_extensions import (
    ensure_currency_matches_unit,
    ensure_target_direction_consistent,
)
from app.domain.enums import KPIDirection, KPIUnit
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class CreateKPICommand:
    """Create KPI command."""

    name: str
    context: RequestContext
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    description: str | None = None
    unit: KPIUnit = KPIUnit.COUNT
    currency: str | None = None
    direction: KPIDirection = KPIDirection.INCREASE
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = None
    refresh_frequency_hours: int | None = None


class CreateKPIUseCase(UseCase[CreateKPICommand, KPIDTO]):
    """Create a KPI scoped to the caller's organization."""

    def execute(self, command: CreateKPICommand) -> KPIDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        org_id = command.context.organization_id
        if org_id is None:
            raise ConflictError(
                "KPIs can only be created within an organization context"
            )

        ensure_currency_matches_unit(command.unit.value, command.currency)
        ensure_target_direction_consistent(
            command.baseline_value, command.target_value, command.direction.value
        )

        with self._uow_factory() as uow:
            validator = KPIValidator(uow)
            validator.ensure_unique_name(org_id, command.name)
            validator.ensure_owner_in_org(command.owner_id, org_id)
            validator.ensure_outcome_in_org(command.outcome_id, org_id)

            kpi = KPI(
                organization_id=org_id,
                outcome_id=command.outcome_id,
                owner_id=command.owner_id,
                name=command.name.strip(),
                description=command.description,
                unit=command.unit,
                currency=command.currency,
                direction=command.direction,
                baseline_value=command.baseline_value,
                target_value=command.target_value,
                current_value=command.current_value,
                data_source=command.data_source,
                refresh_frequency_hours=command.refresh_frequency_hours,
                is_active=True,
            )
            created = uow.kpis.add(kpi)
            uow.commit()
            return kpi_to_dto(created)
```

### backend/app/application/use_cases/kpis/update_kpi.py

```python
"""Update KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.application.validators.kpi_validator import KPIValidator
from app.core.exceptions import NotFoundError
from app.domain.entities.kpi_extensions import (
    KPILifecycle,
    ensure_baseline_stable,
    ensure_target_direction_consistent,
)
from app.domain.enums import KPIDirection
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateKPICommand:
    """Update KPI command."""

    kpi_id: UUID
    context: RequestContext
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    direction: KPIDirection | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    data_source: str | None = None
    refresh_frequency_hours: int | None = None
    is_active: bool | None = None
    _outcome_provided: bool = False
    _owner_provided: bool = False
    _name_provided: bool = False
    _description_provided: bool = False
    _direction_provided: bool = False
    _baseline_provided: bool = False
    _target_provided: bool = False
    _current_provided: bool = False
    _data_source_provided: bool = False
    _refresh_provided: bool = False
    _is_active_provided: bool = False


class UpdateKPIUseCase(UseCase[UpdateKPICommand, KPIDTO]):
    """Update a KPI."""

    def execute(self, command: UpdateKPICommand) -> KPIDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )
            KPILifecycle.ensure_editable(kpi)

            validator = KPIValidator(uow)

            if command._name_provided and command.name is not None:
                validator.ensure_unique_name(
                    kpi.organization_id, command.name, exclude_id=kpi.id
                )
                kpi.name = command.name.strip()

            if command._description_provided:
                kpi.description = command.description

            if command._outcome_provided:
                validator.ensure_outcome_in_org(command.outcome_id, kpi.organization_id)
                kpi.outcome_id = command.outcome_id

            if command._owner_provided:
                validator.ensure_owner_in_org(command.owner_id, kpi.organization_id)
                kpi.owner_id = command.owner_id

            if command._direction_provided and command.direction is not None:
                kpi.direction = command.direction

            if command._baseline_provided:
                ensure_baseline_stable(kpi, command.baseline_value)
                kpi.baseline_value = command.baseline_value

            if command._target_provided:
                kpi.target_value = command.target_value

            if command._current_provided:
                kpi.current_value = command.current_value

            if command._data_source_provided:
                kpi.data_source = command.data_source

            if command._refresh_provided:
                kpi.refresh_frequency_hours = command.refresh_frequency_hours

            if command._is_active_provided and command.is_active is not None:
                if command.is_active:
                    kpi.activate()
                else:
                    kpi.deactivate()

            ensure_target_direction_consistent(
                kpi.baseline_value, kpi.target_value, kpi.direction.value
            )

            kpi.touch()
            updated = uow.kpis.update(kpi)
            uow.commit()
            return kpi_to_dto(updated)
```

### backend/app/application/use_cases/kpis/delete_kpi.py

```python
"""Delete KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.use_cases.base import UseCase
from app.application.validators.kpi_validator import KPIValidator
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class DeleteKPICommand:
    """Soft-delete a KPI."""

    kpi_id: UUID
    context: RequestContext


class DeleteKPIUseCase(UseCase[DeleteKPICommand, None]):
    """Soft-delete a KPI after enforcing business rules."""

    def execute(self, command: DeleteKPICommand) -> None:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )

            KPIValidator(uow).ensure_deletable(kpi.id)

            # Detach from any key results that reference this KPI so those
            # remain valid at the objective level.
            for key_result in uow.key_results.list_by_kpi(kpi.id):
                key_result.kpi_id = None
                key_result.touch()
                uow.key_results.update(key_result)

            uow.kpis.delete(command.kpi_id)
            uow.commit()
```

### backend/app/application/use_cases/kpis/get_kpi.py

```python
"""Get KPI use case."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class GetKPIQuery:
    """Query for a single KPI."""

    kpi_id: UUID
    context: RequestContext


class GetKPIUseCase(UseCase[GetKPIQuery, KPIDTO]):
    """Retrieve a KPI by ID."""

    def execute(self, query: GetKPIQuery) -> KPIDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.KPI_READ)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(query.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {query.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, kpi.organization_id
            )
            return kpi_to_dto(kpi)
```

### backend/app/application/use_cases/kpis/list_kpis.py

```python
"""List KPIs use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.domain.repositories.specifications import KPIFilter, PageRequest
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListKPIsQuery:
    """Filter + pagination query for KPIs."""

    context: RequestContext
    page: PageDTO = field(default_factory=PageDTO)
    outcome_id: UUID | None = None
    owner_id: UUID | None = None
    units: tuple[str, ...] = ()
    is_active: bool | None = None


class ListKPIsUseCase(UseCase[ListKPIsQuery, PaginatedResultDTO[KPIDTO]]):
    """List KPIs for the caller's organization."""

    def execute(self, query: ListKPIsQuery) -> PaginatedResultDTO[KPIDTO]:
        PermissionRegistry.ensure(query.context.actor, Permission.KPI_READ)

        page = PageRequest(
            limit=query.page.limit,
            offset=query.page.offset,
            order_by=query.page.order_by,
            descending=query.page.descending,
        )
        spec = KPIFilter(
            organization_id=query.context.organization_id,
            outcome_id=query.outcome_id,
            owner_id=query.owner_id,
            units=query.units,
            is_active=query.is_active,
        )

        with self._uow_factory() as uow:
            items = uow.kpis.find(spec, page)
            total = uow.kpis.count(spec)

        return PaginatedResultDTO[KPIDTO](
            items=[kpi_to_dto(k) for k in items],
            total=total,
            limit=page.limit,
            offset=page.offset,
        )
```

### backend/app/application/use_cases/kpis/record_snapshot.py

```python
"""Record KPI snapshot use case."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import MetricSnapshotDTO
from app.application.mappers import metric_snapshot_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError, ValidationError
from app.domain.entities.kpi import MetricSnapshot
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class RecordKPISnapshotCommand:
    """Command to record a KPI metric snapshot."""

    kpi_id: UUID
    value: Decimal
    context: RequestContext
    recorded_at: datetime | None = None
    source: str | None = None
    notes: str | None = None
    context_metadata: dict[str, str] = field(default_factory=dict)


class RecordKPISnapshotUseCase(
    UseCase[RecordKPISnapshotCommand, MetricSnapshotDTO]
):
    """Record a new metric snapshot for a KPI and update its current value."""

    def execute(
        self, command: RecordKPISnapshotCommand
    ) -> MetricSnapshotDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )

            if not kpi.is_active:
                raise BusinessRuleViolationError(
                    "Cannot record snapshots for an inactive KPI"
                )

            recorded_at = command.recorded_at or datetime.now(timezone.utc)
            if recorded_at.tzinfo is None:
                recorded_at = recorded_at.replace(tzinfo=timezone.utc)
            if recorded_at > datetime.now(timezone.utc):
                raise ValidationError("Snapshot recorded_at cannot be in the future")

            snapshot = MetricSnapshot(
                kpi_id=kpi.id,
                value=command.value,
                recorded_at=recorded_at,
                source=command.source,
                notes=command.notes,
                context=dict(command.context_metadata),
            )
            created = uow.metric_snapshots.add(snapshot)

            latest = uow.metric_snapshots.latest_for_kpi(kpi.id)
            if latest is None or latest.recorded_at <= created.recorded_at:
                kpi.record_current_value(command.value)
                uow.kpis.update(kpi)

            uow.commit()
            return metric_snapshot_to_dto(created)
```

### backend/app/application/use_cases/kpis/update_target.py

```python
"""Update KPI target value use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi import KPIDTO
from app.application.mappers import kpi_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import BusinessRuleViolationError, NotFoundError, ValidationError
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.kpi_extensions import (
    KPILifecycle,
    ensure_target_direction_consistent,
)
from app.domain.enums import AuditAction
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class UpdateKPITargetCommand:
    """Update a KPI's target value and record the change."""

    kpi_id: UUID
    target_value: Decimal
    context: RequestContext
    reason: str | None = None


class UpdateKPITargetUseCase(UseCase[UpdateKPITargetCommand, KPIDTO]):
    """Update the target of a KPI while auditing the change."""

    def execute(self, command: UpdateKPITargetCommand) -> KPIDTO:
        PermissionRegistry.ensure(command.context.actor, Permission.KPI_MANAGE)

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(command.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {command.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                command.context.actor, kpi.organization_id
            )
            KPILifecycle.ensure_editable(kpi)

            if not kpi.is_active:
                raise BusinessRuleViolationError(
                    "Cannot change target for an inactive KPI"
                )
            if kpi.target_value == command.target_value:
                raise ValidationError(
                    "New target value must differ from the current target"
                )

            ensure_target_direction_consistent(
                kpi.baseline_value, command.target_value, kpi.direction.value
            )

            previous = kpi.target_value
            kpi.target_value = command.target_value
            kpi.touch()
            updated = uow.kpis.update(kpi)

            audit_entry = AuditLog(
                organization_id=kpi.organization_id,
                actor_id=command.context.actor_id,
                action=AuditAction.UPDATE,
                resource_type="kpi.target",
                resource_id=kpi.id,
                ip_address=command.context.ip_address,
                user_agent=command.context.user_agent,
                changes={
                    "previous_target": str(previous) if previous is not None else None,
                    "new_target": str(command.target_value),
                },
                metadata={
                    "reason": command.reason or "",
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            uow.audit_logs.add(audit_entry)

            uow.commit()
            return kpi_to_dto(updated)
```

### backend/app/application/use_cases/kpis/list_history.py

```python
"""List KPI snapshot history use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.context import RequestContext
from app.application.dtos.kpi_extensions import KPIHistoryDTO
from app.application.mappers import kpi_to_dto, metric_snapshot_to_dto
from app.application.use_cases.base import UseCase
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.repositories.specifications import (
    MetricSnapshotFilter,
    PageRequest,
)
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.services.permissions import Permission, PermissionRegistry


@dataclass(frozen=True)
class ListKPIHistoryQuery:
    """Filter + pagination query for KPI history."""

    kpi_id: UUID
    context: RequestContext
    limit: int = 100
    offset: int = 0
    recorded_after: datetime | None = None
    recorded_before: datetime | None = None
    source: str | None = None


class ListKPIHistoryUseCase(UseCase[ListKPIHistoryQuery, KPIHistoryDTO]):
    """Return the historical snapshots for a KPI."""

    def execute(self, query: ListKPIHistoryQuery) -> KPIHistoryDTO:
        PermissionRegistry.ensure(query.context.actor, Permission.KPI_READ)

        if query.limit <= 0 or query.limit > 1000:
            raise ValidationError("limit must be between 1 and 1000")
        if query.offset < 0:
            raise ValidationError("offset cannot be negative")

        with self._uow_factory() as uow:
            kpi = uow.kpis.get_by_id(query.kpi_id)
            if kpi is None:
                raise NotFoundError(f"KPI {query.kpi_id} not found")

            AuthorizationDomainService.ensure_same_organization(
                query.context.actor, kpi.organization_id
            )

            spec = MetricSnapshotFilter(
                kpi_id=kpi.id,
                recorded_after=query.recorded_after,
                recorded_before=query.recorded_before,
                source=query.source,
            )
            page = PageRequest(
                limit=query.limit,
                offset=query.offset,
                order_by="recorded_at",
                descending=True,
            )
            snapshots = uow.metric_snapshots.find(spec, page)

            snapshot_dtos = [metric_snapshot_to_dto(s) for s in snapshots]
            earliest = min((s.recorded_at for s in snapshots), default=None)
            latest = max((s.recorded_at for s in snapshots), default=None)

            return KPIHistoryDTO(
                kpi=kpi_to_dto(kpi),
                snapshots=snapshot_dtos,
                count=len(snapshot_dtos),
                earliest_at=earliest,
                latest_at=latest,
            )
```

### backend/app/api/routers/kpis.py

```python
"""KPI endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.kpi import (
    KPICreateDTO,
    KPIDTO,
    KPIUpdateDTO,
    MetricSnapshotDTO,
)
from app.application.dtos.kpi_extensions import (
    KPIHistoryDTO,
    KPIRecordSnapshotDTO,
    KPIReplaceDTO,
    KPITargetUpdateDTO,
)
from app.application.use_cases.kpis import (
    CreateKPICommand,
    CreateKPIUseCase,
    DeleteKPICommand,
    DeleteKPIUseCase,
    GetKPIQuery,
    GetKPIUseCase,
    ListKPIHistoryQuery,
    ListKPIHistoryUseCase,
    ListKPIsQuery,
    ListKPIsUseCase,
    RecordKPISnapshotCommand,
    RecordKPISnapshotUseCase,
    UpdateKPICommand,
    UpdateKPIUseCase,
    UpdateKPITargetCommand,
    UpdateKPITargetUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import KPIUnit
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.post(
    "",
    response_model=KPIDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a KPI",
)
def create_kpi(
    payload: KPICreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Create a KPI."""
    use_case = CreateKPIUseCase()
    return use_case.execute(
        CreateKPICommand(
            name=payload.name,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            description=payload.description,
            unit=payload.unit,
            currency=payload.currency,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[KPIDTO],
    status_code=status.HTTP_200_OK,
    summary="List KPIs",
)
def list_kpis(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    outcome_id: UUID | None = Query(default=None),
    owner_id: UUID | None = Query(default=None),
    unit: list[KPIUnit] | None = Query(default=None),
    is_active: bool | None = Query(default=None),
) -> PaginatedResultDTO[KPIDTO]:
    """List KPIs with filtering."""
    use_case = ListKPIsUseCase()
    return use_case.execute(
        ListKPIsQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            outcome_id=outcome_id,
            owner_id=owner_id,
            units=tuple(u.value for u in unit) if unit else (),
            is_active=is_active,
        )
    )


@router.get(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a KPI",
)
def get_kpi(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
) -> KPIDTO:
    """Retrieve a KPI by ID."""
    use_case = GetKPIUseCase()
    return use_case.execute(GetKPIQuery(kpi_id=kpi_id, context=context))


@router.patch(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a KPI",
)
def patch_kpi(
    kpi_id: UUID,
    payload: KPIUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Partially update a KPI."""
    provided = payload.model_fields_set
    use_case = UpdateKPIUseCase()
    return use_case.execute(
        UpdateKPICommand(
            kpi_id=kpi_id,
            context=context,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            name=payload.name,
            description=payload.description,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            is_active=payload.is_active,
            _outcome_provided="outcome_id" in provided,
            _owner_provided="owner_id" in provided,
            _name_provided="name" in provided,
            _description_provided="description" in provided,
            _direction_provided="direction" in provided,
            _baseline_provided="baseline_value" in provided,
            _target_provided="target_value" in provided,
            _current_provided="current_value" in provided,
            _data_source_provided="data_source" in provided,
            _refresh_provided="refresh_frequency_hours" in provided,
            _is_active_provided="is_active" in provided,
        )
    )


@router.put(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a KPI (full update)",
)
def replace_kpi(
    kpi_id: UUID,
    payload: KPIReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Full-replacement update of a KPI (baseline changes are still guarded)."""
    use_case = UpdateKPIUseCase()
    return use_case.execute(
        UpdateKPICommand(
            kpi_id=kpi_id,
            context=context,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            name=payload.name,
            description=payload.description,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            is_active=payload.is_active,
            _outcome_provided=True,
            _owner_provided=True,
            _name_provided=True,
            _description_provided=True,
            _direction_provided=True,
            _baseline_provided=True,
            _target_provided=True,
            _current_provided=True,
            _data_source_provided=True,
            _refresh_provided=True,
            _is_active_provided=True,
        )
    )


@router.delete(
    "/{kpi_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a KPI",
)
def delete_kpi(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> None:
    """Soft-delete a KPI."""
    use_case = DeleteKPIUseCase()
    use_case.execute(DeleteKPICommand(kpi_id=kpi_id, context=context))


@router.post(
    "/{kpi_id}/snapshots",
    response_model=MetricSnapshotDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Record a KPI snapshot",
)
def record_snapshot(
    kpi_id: UUID,
    payload: KPIRecordSnapshotDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> MetricSnapshotDTO:
    """Record a new metric snapshot for a KPI."""
    use_case = RecordKPISnapshotUseCase()
    return use_case.execute(
        RecordKPISnapshotCommand(
            kpi_id=kpi_id,
            value=payload.value,
            recorded_at=payload.recorded_at,
            source=payload.source,
            notes=payload.notes,
            context=context,
        )
    )


@router.get(
    "/{kpi_id}/history",
    response_model=KPIHistoryDTO,
    status_code=status.HTTP_200_OK,
    summary="Get KPI snapshot history",
)
def get_history(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    recorded_after: datetime | None = Query(default=None),
    recorded_before: datetime | None = Query(default=None),
    source: str | None = Query(default=None, max_length=200),
) -> KPIHistoryDTO:
    """Return the historical snapshots for a KPI."""
    use_case = ListKPIHistoryUseCase()
    return use_case.execute(
        ListKPIHistoryQuery(
            kpi_id=kpi_id,
            context=context,
            limit=limit,
            offset=offset,
            recorded_after=recorded_after,
            recorded_before=recorded_before,
            source=source,
        )
    )


@router.patch(
    "/{kpi_id}/target",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a KPI's target value (audited)",
)
def update_kpi_target(
    kpi_id: UUID,
    payload: KPITargetUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Update a KPI's target value and record an audit entry."""
    use_case = UpdateKPITargetUseCase()
    return use_case.execute(
        UpdateKPITargetCommand(
            kpi_id=kpi_id,
            target_value=payload.target_value,
            reason=payload.reason,
            context=context,
        )
    )
```

================================================================================

### backend/app/api/main.py

```python
"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import register_exception_handlers
from app.api.lifespan import lifespan
from app.api.middleware.authentication import AuthenticationMiddleware
from app.api.middleware.request_context import RequestContextMiddleware
from app.api.routers.auth import router as auth_router
from app.api.routers.auth_sessions import router as auth_sessions_router
from app.api.routers.business_outcomes import router as business_outcomes_router
from app.api.routers.health import router as health_router
from app.api.routers.kpis import router as kpis_router
from app.api.routers.organizations import router as organizations_router
from app.api.routers.projects import router as projects_router
from app.api.routers.sprints import router as sprints_router
from app.api.routers.teams import router as teams_router
from app.api.routers.users import router as users_router
from app.api.routers.work_items import router as work_items_router
from app.core.config import settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(AuthenticationMiddleware)

    register_exception_handlers(app)

    app.include_router(health_router, prefix=settings.API_V1_PREFIX)
    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(auth_sessions_router, prefix=settings.API_V1_PREFIX)
    app.include_router(organizations_router, prefix=settings.API_V1_PREFIX)
    app.include_router(teams_router, prefix=settings.API_V1_PREFIX)
    app.include_router(users_router, prefix=settings.API_V1_PREFIX)
    app.include_router(projects_router, prefix=settings.API_V1_PREFIX)
    app.include_router(sprints_router, prefix=settings.API_V1_PREFIX)
    app.include_router(work_items_router, prefix=settings.API_V1_PREFIX)
    app.include_router(business_outcomes_router, prefix=settings.API_V1_PREFIX)
    app.include_router(kpis_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
```

### backend/app/api/schemas/common.py

```python
"""Common API response schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response body."""

    error: str = Field(description="Machine-readable error code")
    message: str = Field(description="Human-readable message")
    details: dict[str, Any] = Field(default_factory=dict)


class MessageResponse(BaseModel):
    """Simple message envelope."""

    message: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    environment: str
```

### backend/app/api/routers/teams.py

```python
"""Team endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.api.schemas.common import MessageResponse
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.organization import TeamCreateDTO, TeamDTO, TeamUpdateDTO
from app.application.mappers import team_to_dto
from app.core.exceptions import ConflictError, NotFoundError
from app.domain.entities.organization import Team
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post(
    "",
    response_model=TeamDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a team in the caller's organization",
)
def create_team(
    payload: TeamCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Create a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to create teams",
    )
    if context.organization_id is None:
        raise ConflictError("Team creation requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        if uow.teams.slug_exists(context.organization_id, payload.slug):
            raise ConflictError(f"Team slug '{payload.slug}' is already in use")

        team = Team(
            organization_id=context.organization_id,
            name=payload.name,
            slug=Slug(payload.slug),
            description=payload.description,
        )
        created = uow.teams.add(team)
        uow.commit()
        return team_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[TeamDTO],
    status_code=status.HTTP_200_OK,
    summary="List teams in the caller's organization",
)
def list_teams(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[TeamDTO]:
    """List teams in the organization."""
    if context.organization_id is None:
        return PaginatedResultDTO[TeamDTO](items=[], total=0, limit=limit, offset=offset)

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        items = uow.teams.list_by_organization(context.organization_id, page)
        total = uow.teams.count_by_organization(context.organization_id)

    return PaginatedResultDTO[TeamDTO](
        items=[team_to_dto(t) for t in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{team_id}",
    response_model=TeamDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a team",
)
def get_team(
    team_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Retrieve a team."""
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        return team_to_dto(team)


@router.patch(
    "/{team_id}",
    response_model=TeamDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a team",
)
def update_team(
    team_id: UUID,
    payload: TeamUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> TeamDTO:
    """Update a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to update teams",
    )
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )

        if payload.name is not None:
            team.rename(payload.name)
        if payload.description is not None:
            team.description = payload.description
            team.touch()

        updated = uow.teams.update(team)
        uow.commit()
        return team_to_dto(updated)


@router.delete(
    "/{team_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete (soft) a team",
)
def delete_team(
    team_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> MessageResponse:
    """Soft-delete a team."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_organization(context.actor),
        "You do not have permission to delete teams",
    )
    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(team_id)
        if team is None:
            raise NotFoundError(f"Team {team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        uow.teams.delete(team_id)
        uow.commit()

    return MessageResponse(message="Team deleted successfully")
```

### backend/app/api/routers/projects.py

```python
"""Project endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.api.schemas.common import MessageResponse
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.project import ProjectCreateDTO, ProjectDTO, ProjectUpdateDTO
from app.application.mappers import project_to_dto
from app.core.exceptions import ConflictError, NotFoundError
from app.domain.entities.project import Project
from app.domain.repositories.specifications import PageRequest
from app.domain.services.authorization_service import AuthorizationDomainService
from app.domain.value_objects import Slug
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
)
def create_project(
    payload: ProjectCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Create a new project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to create projects",
    )
    if context.organization_id is None:
        raise ConflictError("Project creation requires an organization context")

    with SQLAlchemyUnitOfWork() as uow:
        team = uow.teams.get_by_id(payload.team_id)
        if team is None:
            raise NotFoundError(f"Team {payload.team_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, team.organization_id
        )
        if uow.projects.key_exists(context.organization_id, payload.key):
            raise ConflictError(f"Project key '{payload.key}' is already in use")
        if uow.projects.slug_exists(context.organization_id, payload.slug):
            raise ConflictError(f"Project slug '{payload.slug}' is already in use")

        project = Project(
            organization_id=context.organization_id,
            team_id=payload.team_id,
            name=payload.name,
            key=payload.key,
            slug=Slug(payload.slug),
            description=payload.description,
            start_date=payload.start_date,
            target_end_date=payload.target_end_date,
        )
        created = uow.projects.add(project)
        uow.commit()
        return project_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[ProjectDTO],
    status_code=status.HTTP_200_OK,
    summary="List projects",
)
def list_projects(
    context: Annotated[RequestContext, Depends(get_request_context)],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    team_id: UUID | None = Query(default=None),
    include_archived: bool = Query(default=False),
) -> PaginatedResultDTO[ProjectDTO]:
    """List projects."""
    if context.organization_id is None:
        return PaginatedResultDTO[ProjectDTO](
            items=[], total=0, limit=limit, offset=offset
        )

    page = PageRequest(limit=limit, offset=offset)
    with SQLAlchemyUnitOfWork() as uow:
        if team_id is not None:
            team = uow.teams.get_by_id(team_id)
            if team is None:
                raise NotFoundError(f"Team {team_id} not found")
            AuthorizationDomainService.ensure_same_organization(
                context.actor, team.organization_id
            )
            items = uow.projects.list_by_team(team_id, page, include_archived)
        else:
            items = uow.projects.list_by_organization(
                context.organization_id, page, include_archived
            )
        total = uow.projects.count_by_organization(
            context.organization_id, include_archived
        )

    return PaginatedResultDTO[ProjectDTO](
        items=[project_to_dto(p) for p in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a project",
)
def get_project(
    project_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Retrieve a project."""
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        return project_to_dto(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a project",
)
def update_project(
    project_id: UUID,
    payload: ProjectUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ProjectDTO:
    """Update a project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to update projects",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        if payload.name is not None:
            project.rename(payload.name)
        if payload.description is not None:
            project.description = payload.description
            project.touch()
        if payload.start_date is not None:
            project.start_date = payload.start_date
            project.touch()
        if payload.target_end_date is not None:
            project.target_end_date = payload.target_end_date
            project.touch()
        if payload.is_archived is not None:
            if payload.is_archived:
                project.archive()
            else:
                project.unarchive()

        updated = uow.projects.update(project)
        uow.commit()
        return project_to_dto(updated)


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete (soft) a project",
)
def delete_project(
    project_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> MessageResponse:
    """Soft-delete a project."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_projects(context.actor),
        "You do not have permission to delete projects",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        uow.projects.delete(project_id)
        uow.commit()

    return MessageResponse(message="Project deleted successfully")
```

### backend/app/api/routers/sprints.py

```python
"""Sprint endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_request_context
from app.api.schemas.common import MessageResponse
from app.application.context import RequestContext
from app.application.dtos.common import PaginatedResultDTO
from app.application.dtos.sprint import (
    SprintCompleteDTO,
    SprintCreateDTO,
    SprintDTO,
    SprintUpdateDTO,
)
from app.application.mappers import sprint_to_dto
from app.core.exceptions import BusinessRuleViolationError, NotFoundError
from app.domain.entities.sprint import Sprint
from app.domain.repositories.specifications import PageRequest, SprintFilter
from app.domain.services.authorization_service import AuthorizationDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.post(
    "",
    response_model=SprintDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a sprint",
)
def create_sprint(
    payload: SprintCreateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Create a new sprint."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to create sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(payload.project_id)
        if project is None:
            raise NotFoundError(f"Project {payload.project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        sprint = Sprint(
            project_id=payload.project_id,
            name=payload.name,
            goal=payload.goal,
            start_date=payload.start_date,
            end_date=payload.end_date,
            planned_capacity=payload.planned_capacity,
        )
        created = uow.sprints.add(sprint)
        uow.commit()
        return sprint_to_dto(created)


@router.get(
    "",
    response_model=PaginatedResultDTO[SprintDTO],
    status_code=status.HTTP_200_OK,
    summary="List sprints for a project",
)
def list_sprints(
    context: Annotated[RequestContext, Depends(get_request_context)],
    project_id: UUID = Query(...),
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResultDTO[SprintDTO]:
    """List sprints in a project."""
    page = PageRequest(limit=limit, offset=offset, order_by="start_date")
    with SQLAlchemyUnitOfWork() as uow:
        project = uow.projects.get_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Project {project_id} not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        items = uow.sprints.list_by_project(project_id, page)
        total = uow.sprints.count(SprintFilter(project_id=project_id))

    return PaginatedResultDTO[SprintDTO](
        items=[sprint_to_dto(s) for s in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{sprint_id}",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a sprint",
)
def get_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Retrieve a sprint."""
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        return sprint_to_dto(sprint)


@router.patch(
    "/{sprint_id}",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a sprint",
)
def update_sprint(
    sprint_id: UUID,
    payload: SprintUpdateDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Update sprint fields."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to update sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )

        if payload.name is not None:
            sprint.name = payload.name
        if payload.goal is not None:
            sprint.goal = payload.goal
        if payload.start_date is not None:
            sprint.start_date = payload.start_date
        if payload.end_date is not None:
            sprint.end_date = payload.end_date
        if payload.planned_capacity is not None:
            sprint.planned_capacity = payload.planned_capacity
        sprint.touch()

        if sprint.end_date < sprint.start_date:
            raise BusinessRuleViolationError("end_date cannot be before start_date")

        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.post(
    "/{sprint_id}/start",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Start a sprint",
)
def start_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Transition a sprint into the active state."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to start sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        if uow.sprints.get_active_for_project(sprint.project_id) is not None:
            raise BusinessRuleViolationError(
                "Another sprint is already active in this project"
            )
        sprint.start()
        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.post(
    "/{sprint_id}/complete",
    response_model=SprintDTO,
    status_code=status.HTTP_200_OK,
    summary="Complete a sprint",
)
def complete_sprint(
    sprint_id: UUID,
    payload: SprintCompleteDTO,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> SprintDTO:
    """Mark a sprint as completed with a final velocity."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to complete sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        sprint.complete(payload.completed_points)
        updated = uow.sprints.update(sprint)
        uow.commit()
        return sprint_to_dto(updated)


@router.delete(
    "/{sprint_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete (soft) a sprint",
)
def delete_sprint(
    sprint_id: UUID,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> MessageResponse:
    """Soft-delete a sprint."""
    AuthorizationDomainService.ensure(
        AuthorizationDomainService.can_manage_sprints(context.actor),
        "You do not have permission to delete sprints",
    )
    with SQLAlchemyUnitOfWork() as uow:
        sprint = uow.sprints.get_by_id(sprint_id)
        if sprint is None:
            raise NotFoundError(f"Sprint {sprint_id} not found")
        project = uow.projects.get_by_id(sprint.project_id)
        if project is None:
            raise NotFoundError("Sprint's project not found")
        AuthorizationDomainService.ensure_same_organization(
            context.actor, project.organization_id
        )
        uow.sprints.delete(sprint_id)
        uow.commit()

    return MessageResponse(message="Sprint deleted successfully")
```

### backend/app/api/routers/work_items.py

```python
"""Work item endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.schemas.common import MessageResponse
from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.work_item import (
    WorkItemCreateDTO,
    WorkItemDTO,
    WorkItemUpdateDTO,
)
from app.application.dtos.work_item_extensions import (
    WorkItemAssignDTO,
    WorkItemMoveDTO,
    WorkItemReplaceDTO,
    WorkItemStatusChangeDTO,
)
from app.application.use_cases.work_items import (
    AssignWorkItemCommand,
    AssignWorkItemUseCase,
    ChangeWorkItemStatusCommand,
    ChangeWorkItemStatusUseCase,
    CreateWorkItemCommand,
    CreateWorkItemUseCase,
    DeleteWorkItemCommand,
    DeleteWorkItemUseCase,
    GetWorkItemQuery,
    GetWorkItemUseCase,
    ListWorkItemsQuery,
    ListWorkItemsUseCase,
    MoveWorkItemToSprintCommand,
    MoveWorkItemToSprintUseCase,
    UpdateWorkItemCommand,
    UpdateWorkItemUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/work-items", tags=["work-items"])


@router.post(
    "",
    response_model=WorkItemDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a work item",
)
def create_work_item(
    payload: WorkItemCreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Create a new work item."""
    use_case = CreateWorkItemUseCase()
    return use_case.execute(
        CreateWorkItemCommand(
            project_id=payload.project_id,
            title=payload.title,
            description=payload.description,
            item_type=payload.item_type,
            priority=payload.priority,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            external_key=payload.external_key,
            labels=list(payload.labels),
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[WorkItemDTO],
    status_code=status.HTTP_200_OK,
    summary="List work items",
)
def list_work_items(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    project_id: UUID | None = Query(default=None),
    sprint_id: UUID | None = Query(default=None),
    assignee_id: UUID | None = Query(default=None),
    reporter_id: UUID | None = Query(default=None),
    epic_id: UUID | None = Query(default=None),
    item_type: list[WorkItemType] | None = Query(default=None),
    status_filter: list[WorkItemStatus] | None = Query(default=None, alias="status"),
    priority: list[WorkItemPriority] | None = Query(default=None),
    label: list[str] | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
    completed_after: datetime | None = Query(default=None),
    completed_before: datetime | None = Query(default=None),
) -> PaginatedResultDTO[WorkItemDTO]:
    """List work items with filtering."""
    use_case = ListWorkItemsUseCase()
    return use_case.execute(
        ListWorkItemsQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            project_id=project_id,
            sprint_id=sprint_id,
            assignee_id=assignee_id,
            reporter_id=reporter_id,
            epic_id=epic_id,
            item_types=tuple(t.value for t in item_type) if item_type else (),
            statuses=tuple(s.value for s in status_filter) if status_filter else (),
            priorities=tuple(p.value for p in priority) if priority else (),
            labels=tuple(label) if label else (),
            search=search,
            completed_after=completed_after,
            completed_before=completed_before,
        )
    )


@router.get(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a work item",
)
def get_work_item(
    work_item_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_READ))],
) -> WorkItemDTO:
    """Retrieve a work item by ID."""
    use_case = GetWorkItemUseCase()
    return use_case.execute(
        GetWorkItemQuery(work_item_id=work_item_id, context=context)
    )


@router.patch(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a work item",
)
def patch_work_item(
    work_item_id: UUID,
    payload: WorkItemUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Partially update a work item."""
    provided = payload.model_fields_set
    use_case = UpdateWorkItemUseCase()
    return use_case.execute(
        UpdateWorkItemCommand(
            work_item_id=work_item_id,
            context=context,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            actual_hours=payload.actual_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            labels=payload.labels,
            _sprint_id_provided="sprint_id" in provided,
            _parent_id_provided="parent_id" in provided,
            _epic_id_provided="epic_id" in provided,
            _assignee_id_provided="assignee_id" in provided,
        )
    )


@router.put(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a work item (full update)",
)
def replace_work_item(
    work_item_id: UUID,
    payload: WorkItemReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Full-replacement update of a work item."""
    use_case = UpdateWorkItemUseCase()
    return use_case.execute(
        UpdateWorkItemCommand(
            work_item_id=work_item_id,
            context=context,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            actual_hours=payload.actual_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            labels=payload.labels,
            _sprint_id_provided=True,
            _parent_id_provided=True,
            _epic_id_provided=True,
            _assignee_id_provided=True,
        )
    )


@router.delete(
    "/{work_item_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Soft-delete a work item",
)
def delete_work_item(
    work_item_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> MessageResponse:
    """Soft-delete a work item."""
    use_case = DeleteWorkItemUseCase()
    use_case.execute(
        DeleteWorkItemCommand(work_item_id=work_item_id, context=context)
    )
    return MessageResponse(message="Work item deleted successfully")


@router.patch(
    "/{work_item_id}/assign",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Assign or unassign a work item",
)
def assign_work_item(
    work_item_id: UUID,
    payload: WorkItemAssignDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Reassign a work item to a user."""
    use_case = AssignWorkItemUseCase()
    return use_case.execute(
        AssignWorkItemCommand(
            work_item_id=work_item_id,
            assignee_id=payload.assignee_id,
            context=context,
        )
    )


@router.patch(
    "/{work_item_id}/status",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Change a work item's status",
)
def change_work_item_status(
    work_item_id: UUID,
    payload: WorkItemStatusChangeDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Change the status of a work item."""
    use_case = ChangeWorkItemStatusUseCase()
    return use_case.execute(
        ChangeWorkItemStatusCommand(
            work_item_id=work_item_id,
            target_status=payload.status,
            actual_hours=payload.actual_hours,
            context=context,
        )
    )


@router.patch(
    "/{work_item_id}/move",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Move a work item to a sprint or the backlog",
)
def move_work_item(
    work_item_id: UUID,
    payload: WorkItemMoveDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Move a work item into a sprint or return it to the backlog."""
    use_case = MoveWorkItemToSprintUseCase()
    return use_case.execute(
        MoveWorkItemToSprintCommand(
            work_item_id=work_item_id,
            sprint_id=payload.sprint_id,
            context=context,
        )
    )
```

### backend/app/api/routers/business_outcomes.py

```python
"""Business outcome endpoints."""

from __future__ import annotations

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.schemas.common import MessageResponse
from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.business_outcome_extensions import (
    BusinessOutcomeArchiveDTO,
    BusinessOutcomeDetailDTO,
    BusinessOutcomeReplaceDTO,
)
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.outcome import (
    BusinessOutcomeCreateDTO,
    BusinessOutcomeDTO,
    BusinessOutcomeUpdateDTO,
)
from app.application.use_cases.outcomes import (
    ArchiveBusinessOutcomeCommand,
    ArchiveBusinessOutcomeUseCase,
    CreateBusinessOutcomeCommand,
    CreateBusinessOutcomeUseCase,
    DeleteBusinessOutcomeCommand,
    DeleteBusinessOutcomeUseCase,
    GetBusinessOutcomeQuery,
    GetBusinessOutcomeUseCase,
    ListBusinessOutcomesQuery,
    ListBusinessOutcomesUseCase,
    UpdateBusinessOutcomeCommand,
    UpdateBusinessOutcomeUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import OutcomeStatus
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/business-outcomes", tags=["business-outcomes"])


@router.post(
    "",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a business outcome",
)
def create_outcome(
    payload: BusinessOutcomeCreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Create a business outcome."""
    use_case = CreateBusinessOutcomeUseCase()
    return use_case.execute(
        CreateBusinessOutcomeCommand(
            name=payload.name,
            owner_id=payload.owner_id,
            description=payload.description,
            hypothesis=payload.hypothesis,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[BusinessOutcomeDTO],
    status_code=status.HTTP_200_OK,
    summary="List business outcomes",
)
def list_outcomes(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    owner_id: UUID | None = Query(default=None),
    status_filter: list[OutcomeStatus] | None = Query(default=None, alias="status"),
    target_before: date | None = Query(default=None),
    target_after: date | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
) -> PaginatedResultDTO[BusinessOutcomeDTO]:
    """List business outcomes with filtering."""
    use_case = ListBusinessOutcomesUseCase()
    return use_case.execute(
        ListBusinessOutcomesQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            owner_id=owner_id,
            statuses=tuple(s.value for s in status_filter) if status_filter else (),
            target_before=target_before,
            target_after=target_after,
            search=search,
        )
    )


@router.get(
    "/{outcome_id}",
    response_model=BusinessOutcomeDetailDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a business outcome (with linked KPIs and work items)",
)
def get_outcome(
    outcome_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_READ))],
    include_linked: bool = Query(default=True),
) -> BusinessOutcomeDetailDTO:
    """Retrieve a business outcome by ID."""
    use_case = GetBusinessOutcomeUseCase()
    return use_case.execute(
        GetBusinessOutcomeQuery(
            outcome_id=outcome_id,
            context=context,
            include_linked=include_linked,
        )
    )


@router.patch(
    "/{outcome_id}",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a business outcome",
)
def patch_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Partially update a business outcome."""
    provided = payload.model_fields_set
    use_case = UpdateBusinessOutcomeUseCase()
    return use_case.execute(
        UpdateBusinessOutcomeCommand(
            outcome_id=outcome_id,
            context=context,
            name=payload.name,
            description=payload.description,
            hypothesis=payload.hypothesis,
            owner_id=payload.owner_id,
            status=payload.status,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            _name_provided="name" in provided,
            _description_provided="description" in provided,
            _hypothesis_provided="hypothesis" in provided,
            _owner_provided="owner_id" in provided,
            _target_date_provided="target_date" in provided,
            _baseline_value_provided="baseline_value" in provided,
            _target_value_provided="target_value" in provided,
            _current_value_provided="current_value" in provided,
            _confidence_score_provided="confidence_score" in provided,
            _financial_impact_provided="financial_impact_estimate" in provided,
        )
    )


@router.put(
    "/{outcome_id}",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a business outcome (full update)",
)
def replace_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Full-replacement update of a business outcome."""
    use_case = UpdateBusinessOutcomeUseCase()
    return use_case.execute(
        UpdateBusinessOutcomeCommand(
            outcome_id=outcome_id,
            context=context,
            name=payload.name,
            description=payload.description,
            hypothesis=payload.hypothesis,
            owner_id=payload.owner_id,
            status=payload.status,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            _name_provided=True,
            _description_provided=True,
            _hypothesis_provided=True,
            _owner_provided=True,
            _target_date_provided=True,
            _baseline_value_provided=True,
            _target_value_provided=True,
            _current_value_provided=True,
            _confidence_score_provided=True,
            _financial_impact_provided=True,
        )
    )


@router.delete(
    "/{outcome_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Soft-delete a business outcome",
)
def delete_outcome(
    outcome_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> MessageResponse:
    """Soft-delete a business outcome."""
    use_case = DeleteBusinessOutcomeUseCase()
    use_case.execute(
        DeleteBusinessOutcomeCommand(outcome_id=outcome_id, context=context)
    )
    return MessageResponse(message="Business outcome deleted successfully")


@router.patch(
    "/{outcome_id}/archive",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Archive or restore a business outcome",
)
def archive_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeArchiveDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Archive or restore a business outcome."""
    use_case = ArchiveBusinessOutcomeUseCase()
    return use_case.execute(
        ArchiveBusinessOutcomeCommand(
            outcome_id=outcome_id, archived=payload.archived, context=context
        )
    )
```

### backend/app/api/routers/kpis.py

```python
"""KPI endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.schemas.common import MessageResponse
from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.kpi import (
    KPICreateDTO,
    KPIDTO,
    KPIUpdateDTO,
    MetricSnapshotDTO,
)
from app.application.dtos.kpi_extensions import (
    KPIHistoryDTO,
    KPIRecordSnapshotDTO,
    KPIReplaceDTO,
    KPITargetUpdateDTO,
)
from app.application.use_cases.kpis import (
    CreateKPICommand,
    CreateKPIUseCase,
    DeleteKPICommand,
    DeleteKPIUseCase,
    GetKPIQuery,
    GetKPIUseCase,
    ListKPIHistoryQuery,
    ListKPIHistoryUseCase,
    ListKPIsQuery,
    ListKPIsUseCase,
    RecordKPISnapshotCommand,
    RecordKPISnapshotUseCase,
    UpdateKPICommand,
    UpdateKPIUseCase,
    UpdateKPITargetCommand,
    UpdateKPITargetUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import KPIUnit
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.post(
    "",
    response_model=KPIDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a KPI",
)
def create_kpi(
    payload: KPICreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Create a KPI."""
    use_case = CreateKPIUseCase()
    return use_case.execute(
        CreateKPICommand(
            name=payload.name,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            description=payload.description,
            unit=payload.unit,
            currency=payload.currency,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[KPIDTO],
    status_code=status.HTTP_200_OK,
    summary="List KPIs",
)
def list_kpis(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    outcome_id: UUID | None = Query(default=None),
    owner_id: UUID | None = Query(default=None),
    unit: list[KPIUnit] | None = Query(default=None),
    is_active: bool | None = Query(default=None),
) -> PaginatedResultDTO[KPIDTO]:
    """List KPIs with filtering."""
    use_case = ListKPIsUseCase()
    return use_case.execute(
        ListKPIsQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            outcome_id=outcome_id,
            owner_id=owner_id,
            units=tuple(u.value for u in unit) if unit else (),
            is_active=is_active,
        )
    )


@router.get(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a KPI",
)
def get_kpi(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
) -> KPIDTO:
    """Retrieve a KPI by ID."""
    use_case = GetKPIUseCase()
    return use_case.execute(GetKPIQuery(kpi_id=kpi_id, context=context))


@router.patch(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a KPI",
)
def patch_kpi(
    kpi_id: UUID,
    payload: KPIUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Partially update a KPI."""
    provided = payload.model_fields_set
    use_case = UpdateKPIUseCase()
    return use_case.execute(
        UpdateKPICommand(
            kpi_id=kpi_id,
            context=context,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            name=payload.name,
            description=payload.description,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            is_active=payload.is_active,
            _outcome_provided="outcome_id" in provided,
            _owner_provided="owner_id" in provided,
            _name_provided="name" in provided,
            _description_provided="description" in provided,
            _direction_provided="direction" in provided,
            _baseline_provided="baseline_value" in provided,
            _target_provided="target_value" in provided,
            _current_provided="current_value" in provided,
            _data_source_provided="data_source" in provided,
            _refresh_provided="refresh_frequency_hours" in provided,
            _is_active_provided="is_active" in provided,
        )
    )


@router.put(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a KPI (full update)",
)
def replace_kpi(
    kpi_id: UUID,
    payload: KPIReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Full-replacement update of a KPI (baseline changes are still guarded)."""
    use_case = UpdateKPIUseCase()
    return use_case.execute(
        UpdateKPICommand(
            kpi_id=kpi_id,
            context=context,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            name=payload.name,
            description=payload.description,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            is_active=payload.is_active,
            _outcome_provided=True,
            _owner_provided=True,
            _name_provided=True,
            _description_provided=True,
            _direction_provided=True,
            _baseline_provided=True,
            _target_provided=True,
            _current_provided=True,
            _data_source_provided=True,
            _refresh_provided=True,
            _is_active_provided=True,
        )
    )


@router.delete(
    "/{kpi_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Soft-delete a KPI",
)
def delete_kpi(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> MessageResponse:
    """Soft-delete a KPI."""
    use_case = DeleteKPIUseCase()
    use_case.execute(DeleteKPICommand(kpi_id=kpi_id, context=context))
    return MessageResponse(message="KPI deleted successfully")


@router.post(
    "/{kpi_id}/snapshots",
    response_model=MetricSnapshotDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Record a KPI snapshot",
)
def record_snapshot(
    kpi_id: UUID,
    payload: KPIRecordSnapshotDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> MetricSnapshotDTO:
    """Record a new metric snapshot for a KPI."""
    use_case = RecordKPISnapshotUseCase()
    return use_case.execute(
        RecordKPISnapshotCommand(
            kpi_id=kpi_id,
            value=payload.value,
            recorded_at=payload.recorded_at,
            source=payload.source,
            notes=payload.notes,
            context=context,
        )
    )


@router.get(
    "/{kpi_id}/history",
    response_model=KPIHistoryDTO,
    status_code=status.HTTP_200_OK,
    summary="Get KPI snapshot history",
)
def get_history(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    recorded_after: datetime | None = Query(default=None),
    recorded_before: datetime | None = Query(default=None),
    source: str | None = Query(default=None, max_length=200),
) -> KPIHistoryDTO:
    """Return the historical snapshots for a KPI."""
    use_case = ListKPIHistoryUseCase()
    return use_case.execute(
        ListKPIHistoryQuery(
            kpi_id=kpi_id,
            context=context,
            limit=limit,
            offset=offset,
            recorded_after=recorded_after,
            recorded_before=recorded_before,
            source=source,
        )
    )


@router.patch(
    "/{kpi_id}/target",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a KPI's target value (audited)",
)
def update_kpi_target(
    kpi_id: UUID,
    payload: KPITargetUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Update a KPI's target value and record an audit entry."""
    use_case = UpdateKPITargetCommand
    return UpdateKPITargetUseCase().execute(
        UpdateKPITargetCommand(
            kpi_id=kpi_id,
            target_value=payload.target_value,
            reason=payload.reason,
            context=context,
        )
    )
```

### backend/app/api/routers/auth_sessions.py

```python
"""Session management endpoints: refresh, logout, list active sessions."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.schemas.common import MessageResponse
from app.api.security import get_authenticated_user
from app.application.dtos.auth import RefreshTokenDTO, TokenDTO
from app.application.dtos.auth_extended import (
    ChangePasswordDTO,
    LogoutDTO,
    UserSessionDTO,
)
from app.application.services.authentication_service import AuthenticationService
from app.application.use_cases.auth.change_password import (
    ChangePasswordCommand,
    ChangePasswordUseCase,
)
from app.core.config import settings
from app.domain.entities.user import User
from app.domain.repositories.specifications import PageRequest
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token/refresh",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="Rotate a refresh token and issue a new access token",
)
def rotate_refresh_token(payload: RefreshTokenDTO, request: Request) -> TokenDTO:
    """Rotate a refresh token by revoking the presented one and issuing a new pair."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    service = AuthenticationService()
    result = service.refresh(payload.refresh_token, ip_address=ip, user_agent=ua)
    return TokenDTO(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        expires_in=result.expires_in,
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Log out of the current session",
)
def logout(
    payload: LogoutDTO,
    _user: Annotated[User, Depends(get_authenticated_user)],
) -> MessageResponse:
    """Revoke the session backing a refresh token."""
    service = AuthenticationService()
    service.logout(payload.refresh_token)
    return MessageResponse(message="Logged out successfully")


@router.post(
    "/logout-all",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Log out of every active session for the current user",
)
def logout_all(
    user: Annotated[User, Depends(get_authenticated_user)],
) -> MessageResponse:
    """Revoke every active session for the current user."""
    service = AuthenticationService()
    service.logout_all(user.id)
    return MessageResponse(message="All sessions logged out successfully")


@router.get(
    "/sessions",
    response_model=list[UserSessionDTO],
    status_code=status.HTTP_200_OK,
    summary="List the current user's sessions",
)
def list_sessions(
    user: Annotated[User, Depends(get_authenticated_user)],
    limit: int = 20,
    offset: int = 0,
) -> list[UserSessionDTO]:
    """Return the current user's sessions."""
    page = PageRequest(
        limit=min(max(limit, 1), settings.MAX_PAGE_SIZE),
        offset=max(offset, 0),
    )
    with SQLAlchemyUnitOfWork() as uow:
        sessions = uow.user_sessions.list_by_user(user.id, page)
    return [
        UserSessionDTO(
            id=s.id,
            user_id=s.user_id,
            issued_at=s.issued_at,
            expires_at=s.expires_at,
            revoked_at=s.revoked_at,
            ip_address=s.ip_address,
            user_agent=s.user_agent,
            last_used_at=s.last_used_at,
            created_at=s.created_at,
        )
        for s in sessions
    ]


@router.post(
    "/password/change",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Change the current user's password",
)
def change_password(
    payload: ChangePasswordDTO,
    user: Annotated[User, Depends(get_authenticated_user)],
) -> MessageResponse:
    """Change the current user's password and revoke all sessions."""
    use_case = ChangePasswordUseCase()
    use_case.execute(
        ChangePasswordCommand(
            user_id=user.id,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
    )
    return MessageResponse(message="Password changed successfully")
```

### backend/app/api/dependencies.py

```python
"""FastAPI dependency providers."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer

from app.application.context import RequestContext
from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_token
from app.domain.entities.user import User
from app.domain.enums import UserRole
from app.domain.services.authorization_service import AuthorizationDomainService
from app.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork

_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False,
)


def get_uow_factory() -> type[SQLAlchemyUnitOfWork]:
    """Return the concrete Unit-of-Work factory type."""
    return SQLAlchemyUnitOfWork


def get_current_user(
    request: Request,
    token: Annotated[str | None, Depends(_oauth2_scheme)],
) -> User:
    """Resolve the current authenticated user from a Bearer token."""
    if not token:
        raise AuthenticationError("Authentication credentials were not provided")

    payload = decode_token(token)
    if payload.get("type") != "access":
        raise AuthenticationError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise AuthenticationError("Token missing subject")

    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise AuthenticationError("Invalid subject in token") from exc

    with SQLAlchemyUnitOfWork() as uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise AuthenticationError("User not found")
        if not user.is_active:
            raise AuthenticationError("User account is not active")

    request.state.current_user = user
    return user


def get_request_context(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    x_forwarded_for: Annotated[str | None, Header(alias="X-Forwarded-For")] = None,
) -> RequestContext:
    """Build a RequestContext for use cases."""
    ip_address = x_forwarded_for or (request.client.host if request.client else None)
    user_agent = request.headers.get("user-agent")
    return RequestContext(
        actor=current_user,
        ip_address=ip_address,
        user_agent=user_agent,
    )


def require_roles(*roles: UserRole):
    """Return a dependency that requires the current user to have one of the given roles."""

    def _dependency(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in roles:
            raise AuthorizationError(
                f"This action requires one of roles: {', '.join(r.value for r in roles)}"
            )
        return user

    return _dependency


def require_admin(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require an admin-level user."""
    if not AuthorizationDomainService.can_manage_organization(user):
        raise AuthorizationError("Administrator privileges required")
    return user
```

### backend/app/application/services/notification_service.py

```python
"""Notification application service."""

from __future__ import annotations

from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domain.entities.notification import Notification
from app.domain.enums import NotificationChannel, NotificationStatus
from app.domain.repositories.notification_repository import (
    NotificationRepositoryContract,
)


class NotificationService:
    """Creates and dispatches user-facing notifications."""

    def __init__(self, repository: NotificationRepositoryContract) -> None:
        self._repository = repository

    def notify(
        self,
        *,
        recipient_id: UUID,
        organization_id: UUID,
        title: str,
        body: str,
        event_type: str,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        subject_type: str | None = None,
        subject_id: UUID | None = None,
        action_url: str | None = None,
    ) -> Notification:
        """Create a pending notification for a recipient."""
        notification = Notification(
            recipient_id=recipient_id,
            organization_id=organization_id,
            title=title,
            body=body,
            channel=channel,
            status=NotificationStatus.PENDING,
            event_type=event_type,
            subject_type=subject_type,
            subject_id=subject_id,
            action_url=action_url,
        )
        return self._repository.add(notification)

    def mark_read(self, notification_id: UUID) -> Notification:
        """Mark a notification as read."""
        notification = self._repository.get_by_id(notification_id)
        if notification is None:
            raise NotFoundError(f"Notification {notification_id} not found")
        notification.mark_read()
        return self._repository.update(notification)

    def mark_all_read(self, recipient_id: UUID) -> int:
        """Mark all pending/sent notifications for a recipient as read."""
        return self._repository.mark_all_read(recipient_id)
```

### backend/app/application/dtos/business_outcome_extensions.py

```python
"""Extended DTOs for business outcome operations."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.application.dtos.kpi import KPIDTO
from app.application.dtos.outcome import BusinessOutcomeDTO
from app.application.dtos.work_item import WorkItemDTO
from app.domain.enums import OutcomeStatus


class BusinessOutcomeReplaceDTO(BaseModel):
    """Full-replacement (PUT) payload for a business outcome."""

    owner_id: UUID | None = None
    name: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=4000)
    hypothesis: str | None = Field(default=None, max_length=4000)
    status: OutcomeStatus
    target_date: date | None = None
    baseline_value: Decimal | None = None
    target_value: Decimal | None = None
    current_value: Decimal | None = None
    confidence_score: Decimal | None = Field(default=None, ge=0, le=100)
    financial_impact_estimate: Decimal | None = None


class BusinessOutcomeArchiveDTO(BaseModel):
    """Payload for archiving/unarchiving a business outcome."""

    archived: bool = True


class BusinessOutcomeDetailDTO(BaseModel):
    """Aggregated read model for a business outcome with linked children."""

    model_config = ConfigDict(from_attributes=True)

    outcome: BusinessOutcomeDTO
    kpis: list[KPIDTO]
    linked_work_items: list[WorkItemDTO]
    attribution_count: int
    latest_snapshot_at: datetime | None = None
```

================================================================================

### frontend/src/config/routes.ts

```ts
export const ROUTES = {
  ROOT: "/",
  LOGIN: "/login",
  DASHBOARD: "/dashboard",
  ORGANIZATIONS: "/organizations",
  TEAMS: "/teams",
  USERS: "/users",
  PROJECTS: "/projects",
  SPRINTS: "/sprints",
  WORK_ITEMS: "/work-items",
  BUSINESS_OUTCOMES: "/business-outcomes",
  KPIS: "/kpis",
  PROFILE: "/profile",
  NOT_FOUND: "*",
} as const;

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES];

export const PUBLIC_ROUTES: readonly AppRoute[] = [ROUTES.LOGIN] as const;

export const PROTECTED_ROUTES: readonly AppRoute[] = [
  ROUTES.DASHBOARD,
  ROUTES.ORGANIZATIONS,
  ROUTES.TEAMS,
  ROUTES.USERS,
  ROUTES.PROJECTS,
  ROUTES.SPRINTS,
  ROUTES.WORK_ITEMS,
  ROUTES.BUSINESS_OUTCOMES,
  ROUTES.KPIS,
  ROUTES.PROFILE,
] as const;

export const NAVIGATION_ITEMS: ReadonlyArray<{
  label: string;
  path: AppRoute;
}> = [
  { label: "Dashboard", path: ROUTES.DASHBOARD },
  { label: "Organizations", path: ROUTES.ORGANIZATIONS },
  { label: "Teams", path: ROUTES.TEAMS },
  { label: "Users", path: ROUTES.USERS },
  { label: "Projects", path: ROUTES.PROJECTS },
  { label: "Sprints", path: ROUTES.SPRINTS },
  { label: "Work Items", path: ROUTES.WORK_ITEMS },
  { label: "Business Outcomes", path: ROUTES.BUSINESS_OUTCOMES },
  { label: "KPIs", path: ROUTES.KPIS },
] as const;
```

### frontend/src/router/AppRouter.tsx

```tsx
import { lazy, Suspense } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import { ProtectedRoute } from "../components/auth/ProtectedRoute";
import { AppLayout } from "../components/layouts/AppLayout";
import { AuthLayout } from "../components/layouts/AuthLayout";
import { PageLoader } from "../components/ui/PageLoader";
import { ROUTES } from "../config/routes";

const LoginPage = lazy(() => import("../pages/auth/LoginPage"));
const DashboardPage = lazy(() => import("../pages/dashboard/DashboardPage"));
const OrganizationsPage = lazy(
  () => import("../pages/organizations/OrganizationsPage"),
);
const TeamsPage = lazy(() => import("../pages/teams/TeamsPage"));
const UsersPage = lazy(() => import("../pages/users/UsersPage"));
const ProjectsPage = lazy(() => import("../pages/projects/ProjectsPage"));
const SprintsPage = lazy(() => import("../pages/sprints/SprintsPage"));
const WorkItemsPage = lazy(() => import("../pages/work-items/WorkItemsPage"));
const BusinessOutcomesPage = lazy(
  () => import("../pages/business-outcomes/BusinessOutcomesPage"),
);
const KpisPage = lazy(() => import("../pages/kpis/KpisPage"));
const ProfilePage = lazy(() => import("../pages/profile/ProfilePage"));
const NotFoundPage = lazy(() => import("../pages/errors/NotFoundPage"));

export function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route
            path={ROUTES.ROOT}
            element={<Navigate to={ROUTES.DASHBOARD} replace />}
          />

          <Route element={<AuthLayout />}>
            <Route path={ROUTES.LOGIN} element={<LoginPage />} />
          </Route>

          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
            <Route
              path={ROUTES.ORGANIZATIONS}
              element={<OrganizationsPage />}
            />
            <Route path={ROUTES.TEAMS} element={<TeamsPage />} />
            <Route path={ROUTES.USERS} element={<UsersPage />} />
            <Route path={ROUTES.PROJECTS} element={<ProjectsPage />} />
            <Route path={ROUTES.SPRINTS} element={<SprintsPage />} />
            <Route path={ROUTES.WORK_ITEMS} element={<WorkItemsPage />} />
            <Route
              path={ROUTES.BUSINESS_OUTCOMES}
              element={<BusinessOutcomesPage />}
            />
            <Route path={ROUTES.KPIS} element={<KpisPage />} />
            <Route path={ROUTES.PROFILE} element={<ProfilePage />} />
          </Route>

          <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default AppRouter;
```

================================================================================

### frontend/src/router/AppRouter.tsx

```tsx
import { Suspense } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import { AppLayout } from "../components/layout/AppLayout";
import LoginPage from "../pages/auth/LoginPage";
import DashboardPage from "../pages/dashboard/DashboardPage";
import ModulePlaceholder from "../pages/ModulePlaceholder";
import NotFoundPage from "../pages/NotFoundPage";
import { ProtectedRoute } from "./ProtectedRoute";
import { PublicRoute } from "./PublicRoute";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={null}>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          <Route
            path="/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />

          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard" element={<DashboardPage />} />

            <Route
              path="/organizations"
              element={<ModulePlaceholder title="Organizations" />}
            />
            <Route
              path="/teams"
              element={<ModulePlaceholder title="Teams" />}
            />
            <Route
              path="/users"
              element={<ModulePlaceholder title="Users" />}
            />
            <Route
              path="/projects"
              element={<ModulePlaceholder title="Projects" />}
            />
            <Route
              path="/sprints"
              element={<ModulePlaceholder title="Sprints" />}
            />
            <Route
              path="/work-items"
              element={<ModulePlaceholder title="Work Items" />}
            />
            <Route
              path="/business-outcomes"
              element={<ModulePlaceholder title="Business Outcomes" />}
            />
            <Route
              path="/kpis"
              element={<ModulePlaceholder title="KPIs" />}
            />
            <Route
              path="/profile"
              element={<ModulePlaceholder title="Profile" />}
            />
          </Route>

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default AppRouter;
```

================================================================================

### frontend/src/router/AppRouter.tsx

```tsx
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "../components/layout/AppLayout";
import LoginPage from "../pages/auth/LoginPage";
import DashboardPage from "../pages/dashboard/DashboardPage";
import ModulePlaceholder from "../pages/ModulePlaceholder";
import NotFoundPage from "../pages/NotFoundPage";
import { ProtectedRoute } from "./ProtectedRoute";
import { PublicRoute } from "./PublicRoute";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />

        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />

        <Route
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />

          <Route
            path="/organizations"
            element={<ModulePlaceholder title="Organizations" />}
          />
          <Route
            path="/teams"
            element={<ModulePlaceholder title="Teams" />}
          />
          <Route
            path="/users"
            element={<ModulePlaceholder title="Users" />}
          />
          <Route
            path="/projects"
            element={<ModulePlaceholder title="Projects" />}
          />
          <Route
            path="/sprints"
            element={<ModulePlaceholder title="Sprints" />}
          />
          <Route
            path="/work-items"
            element={<ModulePlaceholder title="Work Items" />}
          />
          <Route
            path="/business-outcomes"
            element={<ModulePlaceholder title="Business Outcomes" />}
          />
          <Route path="/kpis" element={<ModulePlaceholder title="KPIs" />} />
          <Route
            path="/profile"
            element={<ModulePlaceholder title="Profile" />}
          />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;
```

================================================================================

### frontend/package.json

```json
{
  "name": "sprint-outcome-tracer-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx,css,json}\""
  },
  "dependencies": {
    "@hookform/resolvers": "^3.9.0",
    "@radix-ui/react-dialog": "^1.1.2",
    "@radix-ui/react-dropdown-menu": "^2.1.2",
    "@radix-ui/react-label": "^2.1.0",
    "@radix-ui/react-slot": "^1.1.0",
    "@radix-ui/react-toast": "^1.2.2",
    "axios": "^1.7.7",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "lucide-react": "^0.451.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-hook-form": "^7.53.0",
    "react-router-dom": "^6.26.2",
    "tailwind-merge": "^2.5.2",
    "tailwindcss-animate": "^1.0.7",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.7.4",
    "@types/react": "^18.3.11",
    "@types/react-dom": "^18.3.0",
    "@typescript-eslint/eslint-plugin": "^8.8.0",
    "@typescript-eslint/parser": "^8.8.0",
    "@vitejs/plugin-react": "^4.3.2",
    "autoprefixer": "^10.4.20",
    "eslint": "^9.11.1",
    "eslint-plugin-react-hooks": "^5.1.0-rc.0",
    "eslint-plugin-react-refresh": "^0.4.12",
    "postcss": "^8.4.47",
    "prettier": "^3.3.3",
    "tailwindcss": "^3.4.13",
    "typescript": "^5.6.2",
    "vite": "^5.4.8"
  }
}
```

### frontend/tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "Bundler",
    "allowImportingTsExtensions": false,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### frontend/tsconfig.node.json

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
```

### frontend/vite.config.ts

```ts
import path from "node:path";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
  },
});
```

### frontend/postcss.config.js

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### frontend/tailwind.config.ts

```ts
import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const config: Config = {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    container: {
      center: true,
      padding: "1rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [animate],
};

export default config;
```

### frontend/index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta
      name="description"
      content="Trace engineering work to measurable business outcomes."
    />
    <title>Sprint Business Outcome Tracer</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### frontend/.env.example

```dotenv
VITE_API_BASE_URL=/api/v1
VITE_APP_NAME=Sprint Business Outcome Tracer
VITE_STORAGE_PREFIX=sbot
```

### frontend/src/main.tsx

```tsx
import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
import "./styles/globals.css";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Root element #root not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

### frontend/src/App.tsx

```tsx
import { AuthProvider } from "./features/auth/AuthProvider";
import { AppRouter } from "./router/AppRouter";
import { ThemeProvider } from "./providers/ThemeProvider";
import { ToastProvider } from "./providers/ToastProvider";

export default function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <AuthProvider>
          <AppRouter />
        </AuthProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}
```

### frontend/src/styles/globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222 47% 11%;
    --card: 0 0% 100%;
    --card-foreground: 222 47% 11%;
    --primary: 221 83% 53%;
    --primary-foreground: 0 0% 100%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222 47% 11%;
    --muted: 210 40% 96%;
    --muted-foreground: 215 16% 47%;
    --accent: 210 40% 96%;
    --accent-foreground: 222 47% 11%;
    --destructive: 0 84% 60%;
    --destructive-foreground: 0 0% 100%;
    --border: 214 32% 91%;
    --input: 214 32% 91%;
    --ring: 221 83% 53%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222 47% 8%;
    --foreground: 210 40% 98%;
    --card: 222 47% 10%;
    --card-foreground: 210 40% 98%;
    --primary: 217 91% 60%;
    --primary-foreground: 222 47% 11%;
    --secondary: 217 33% 17%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217 33% 17%;
    --muted-foreground: 215 20% 65%;
    --accent: 217 33% 17%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 63% 45%;
    --destructive-foreground: 210 40% 98%;
    --border: 217 33% 17%;
    --input: 217 33% 17%;
    --ring: 217 91% 60%;
  }

  * {
    @apply border-border;
  }

  html,
  body,
  #root {
    @apply h-full;
  }

  body {
    @apply bg-background text-foreground antialiased;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}
```

### frontend/src/config/env.ts

```ts
interface AppEnv {
  readonly API_BASE_URL: string;
  readonly APP_NAME: string;
  readonly STORAGE_PREFIX: string;
}

function readEnv(key: string, fallback: string): string {
  const value = import.meta.env[key as keyof ImportMetaEnv] as
    | string
    | undefined;
  return value && value.length > 0 ? value : fallback;
}

export const ENV: AppEnv = {
  API_BASE_URL: readEnv("VITE_API_BASE_URL", "/api/v1"),
  APP_NAME: readEnv("VITE_APP_NAME", "Sprint Business Outcome Tracer"),
  STORAGE_PREFIX: readEnv("VITE_STORAGE_PREFIX", "sbot"),
};
```

### frontend/src/config/routes.ts

```ts
export const ROUTES = {
  ROOT: "/",
  LOGIN: "/login",
  DASHBOARD: "/dashboard",
  ORGANIZATIONS: "/organizations",
  TEAMS: "/teams",
  USERS: "/users",
  PROJECTS: "/projects",
  SPRINTS: "/sprints",
  WORK_ITEMS: "/work-items",
  BUSINESS_OUTCOMES: "/business-outcomes",
  KPIS: "/kpis",
  OKRS: "/okrs",
  REPORTS: "/reports",
  PROFILE: "/profile",
  NOT_FOUND: "*",
} as const;

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES];
```

### frontend/src/config/navigation.ts

```ts
import {
  BarChart3,
  Briefcase,
  Building2,
  Gauge,
  LayoutDashboard,
  ListChecks,
  Target,
  Timer,
  Trophy,
  UserCog,
  Users,
  Users2,
  type LucideIcon,
} from "lucide-react";

import { ROUTES, type AppRoute } from "./routes";

export interface NavigationItem {
  readonly label: string;
  readonly path: AppRoute;
  readonly icon: LucideIcon;
}

export const PRIMARY_NAVIGATION: readonly NavigationItem[] = [
  { label: "Dashboard", path: ROUTES.DASHBOARD, icon: LayoutDashboard },
  { label: "Organizations", path: ROUTES.ORGANIZATIONS, icon: Building2 },
  { label: "Teams", path: ROUTES.TEAMS, icon: Users2 },
  { label: "Users", path: ROUTES.USERS, icon: Users },
  { label: "Projects", path: ROUTES.PROJECTS, icon: Briefcase },
  { label: "Sprints", path: ROUTES.SPRINTS, icon: Timer },
  { label: "Work Items", path: ROUTES.WORK_ITEMS, icon: ListChecks },
  { label: "Business Outcomes", path: ROUTES.BUSINESS_OUTCOMES, icon: Target },
  { label: "KPIs", path: ROUTES.KPIS, icon: Gauge },
  { label: "OKRs", path: ROUTES.OKRS, icon: Trophy },
  { label: "Reports", path: ROUTES.REPORTS, icon: BarChart3 },
] as const;

export const SECONDARY_NAVIGATION: readonly NavigationItem[] = [
  { label: "Profile", path: ROUTES.PROFILE, icon: UserCog },
] as const;
```

### frontend/src/lib/utils.ts

```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
```

### frontend/src/lib/storage.ts

```ts
import { ENV } from "@/config/env";

const PREFIX = ENV.STORAGE_PREFIX;

function key(name: string): string {
  return `${PREFIX}:${name}`;
}

export const storage = {
  get<T = string>(name: string): T | null {
    try {
      const raw = window.localStorage.getItem(key(name));
      if (raw === null) return null;
      try {
        return JSON.parse(raw) as T;
      } catch {
        return raw as unknown as T;
      }
    } catch {
      return null;
    }
  },
  set(name: string, value: unknown): void {
    try {
      const raw = typeof value === "string" ? value : JSON.stringify(value);
      window.localStorage.setItem(key(name), raw);
    } catch {
      /* storage is best-effort */
    }
  },
  remove(name: string): void {
    try {
      window.localStorage.removeItem(key(name));
    } catch {
      /* storage is best-effort */
    }
  },
  clearAll(): void {
    try {
      const toRemove: string[] = [];
      for (let i = 0; i < window.localStorage.length; i += 1) {
        const k = window.localStorage.key(i);
        if (k && k.startsWith(`${PREFIX}:`)) {
          toRemove.push(k);
        }
      }
      toRemove.forEach((k) => window.localStorage.removeItem(k));
    } catch {
      /* storage is best-effort */
    }
  },
};
```

### frontend/src/lib/tokens.ts

```ts
import { storage } from "./storage";

const ACCESS_KEY = "auth.access_token";
const REFRESH_KEY = "auth.refresh_token";

export const tokenStorage = {
  getAccessToken(): string | null {
    return storage.get<string>(ACCESS_KEY);
  },
  getRefreshToken(): string | null {
    return storage.get<string>(REFRESH_KEY);
  },
  setTokens(access: string, refresh: string): void {
    storage.set(ACCESS_KEY, access);
    storage.set(REFRESH_KEY, refresh);
  },
  clear(): void {
    storage.remove(ACCESS_KEY);
    storage.remove(REFRESH_KEY);
  },
};
```

### frontend/src/api/client.ts

```ts
import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig } from "axios";

import { ENV } from "@/config/env";
import { tokenStorage } from "@/lib/tokens";

interface RetriableRequestConfig extends AxiosRequestConfig {
  _retry?: boolean;
}

interface RefreshResponse {
  readonly access_token: string;
  readonly refresh_token: string;
  readonly token_type: string;
  readonly expires_in: number;
}

const UNAUTHORIZED_EVENT = "sbot:unauthorized";

export function emitUnauthorized(): void {
  window.dispatchEvent(new CustomEvent(UNAUTHORIZED_EVENT));
}

export function onUnauthorized(listener: () => void): () => void {
  const handler = () => listener();
  window.addEventListener(UNAUTHORIZED_EVENT, handler);
  return () => window.removeEventListener(UNAUTHORIZED_EVENT, handler);
}

export const apiClient: AxiosInstance = axios.create({
  baseURL: ENV.API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = tokenStorage.getAccessToken();
  if (token) {
    config.headers = config.headers ?? {};
    (config.headers as Record<string, string>).Authorization = `Bearer ${token}`;
  }
  return config;
});

let refreshInFlight: Promise<string | null> | null = null;

async function performRefresh(): Promise<string | null> {
  const refreshToken = tokenStorage.getRefreshToken();
  if (!refreshToken) return null;

  try {
    const response = await axios.post<RefreshResponse>(
      `${ENV.API_BASE_URL}/auth/token/refresh`,
      { refresh_token: refreshToken },
      { headers: { "Content-Type": "application/json" } },
    );
    const { access_token, refresh_token } = response.data;
    tokenStorage.setTokens(access_token, refresh_token);
    return access_token;
  } catch {
    tokenStorage.clear();
    return null;
  }
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as RetriableRequestConfig | undefined;
    const status = error.response?.status;

    if (status === 401 && original && !original._retry) {
      original._retry = true;

      if (!refreshInFlight) {
        refreshInFlight = performRefresh().finally(() => {
          refreshInFlight = null;
        });
      }

      const newToken = await refreshInFlight;
      if (newToken) {
        original.headers = original.headers ?? {};
        (original.headers as Record<string, string>).Authorization =
          `Bearer ${newToken}`;
        return apiClient(original);
      }

      emitUnauthorized();
    }

    return Promise.reject(error);
  },
);
```

### frontend/src/api/endpoints.ts

```ts
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: "/auth/login",
    REFRESH: "/auth/token/refresh",
    LOGOUT: "/auth/logout",
    LOGOUT_ALL: "/auth/logout-all",
    ME: "/auth/me",
    SESSIONS: "/auth/sessions",
    CHANGE_PASSWORD: "/auth/password/change",
  },
  ORGANIZATIONS: "/organizations",
  TEAMS: "/teams",
  USERS: "/users",
  PROJECTS: "/projects",
  SPRINTS: "/sprints",
  WORK_ITEMS: "/work-items",
  BUSINESS_OUTCOMES: "/business-outcomes",
  KPIS: "/kpis",
} as const;
```

### frontend/src/api/errors.ts

```ts
import axios, { type AxiosError } from "axios";

interface ApiErrorPayload {
  readonly error?: string;
  readonly message?: string;
  readonly details?: Record<string, unknown>;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details: Record<string, unknown>;

  constructor(
    message: string,
    status: number,
    code: string,
    details: Record<string, unknown> = {},
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

export function toApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiErrorPayload>;
    const status = axiosError.response?.status ?? 0;
    const payload = axiosError.response?.data;
    const message =
      payload?.message ?? axiosError.message ?? "Unexpected error";
    const code = payload?.error ?? "unknown_error";
    return new ApiError(message, status, code, payload?.details ?? {});
  }
  if (error instanceof Error) {
    return new ApiError(error.message, 0, "unknown_error");
  }
  return new ApiError("Unexpected error", 0, "unknown_error");
}
```

### frontend/src/features/auth/types.ts

```ts
export type UserRole =
  | "super_admin"
  | "org_admin"
  | "executive"
  | "product_manager"
  | "engineering_manager"
  | "engineer"
  | "viewer";

export type UserStatus =
  | "active"
  | "invited"
  | "suspended"
  | "deactivated";

export interface AuthUser {
  readonly id: string;
  readonly email: string;
  readonly full_name: string;
  readonly organization_id: string | null;
  readonly role: UserRole;
  readonly status: UserStatus;
  readonly last_login_at: string | null;
  readonly is_email_verified: boolean;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface TokenPair {
  readonly access_token: string;
  readonly refresh_token: string;
  readonly token_type: string;
  readonly expires_in: number;
}

export interface LoginCredentials {
  readonly email: string;
  readonly password: string;
}
```

### frontend/src/features/auth/authApi.ts

```ts
import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type { AuthUser, LoginCredentials, TokenPair } from "./types";

export const authApi = {
  async login(credentials: LoginCredentials): Promise<TokenPair> {
    const params = new URLSearchParams();
    params.append("username", credentials.email);
    params.append("password", credentials.password);

    const response = await apiClient.post<TokenPair>(
      API_ENDPOINTS.AUTH.LOGIN,
      params,
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      },
    );
    return response.data;
  },

  async me(): Promise<AuthUser> {
    const response = await apiClient.get<AuthUser>(API_ENDPOINTS.AUTH.ME);
    return response.data;
  },

  async logout(refreshToken: string): Promise<void> {
    await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT, {
      refresh_token: refreshToken,
    });
  },
};
```

### frontend/src/features/auth/AuthContext.ts

```ts
import { createContext } from "react";

import type { AuthUser, LoginCredentials } from "./types";

export interface AuthContextValue {
  readonly user: AuthUser | null;
  readonly isAuthenticated: boolean;
  readonly isInitializing: boolean;
  readonly isSubmitting: boolean;
  readonly login: (credentials: LoginCredentials) => Promise<void>;
  readonly logout: () => Promise<void>;
  readonly refreshCurrentUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
);
```

### frontend/src/features/auth/AuthProvider.tsx

```tsx
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { onUnauthorized } from "@/api/client";
import { toApiError } from "@/api/errors";
import { tokenStorage } from "@/lib/tokens";

import { AuthContext, type AuthContextValue } from "./AuthContext";
import { authApi } from "./authApi";
import type { AuthUser, LoginCredentials } from "./types";

interface AuthProviderProps {
  readonly children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isInitializing, setIsInitializing] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const mounted = useRef<boolean>(true);

  const refreshCurrentUser = useCallback(async () => {
    const token = tokenStorage.getAccessToken();
    if (!token) {
      setUser(null);
      return;
    }
    try {
      const me = await authApi.me();
      if (mounted.current) setUser(me);
    } catch {
      tokenStorage.clear();
      if (mounted.current) setUser(null);
    }
  }, []);

  useEffect(() => {
    mounted.current = true;
    void (async () => {
      await refreshCurrentUser();
      if (mounted.current) setIsInitializing(false);
    })();
    return () => {
      mounted.current = false;
    };
  }, [refreshCurrentUser]);

  useEffect(() => {
    const off = onUnauthorized(() => {
      tokenStorage.clear();
      setUser(null);
    });
    return off;
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setIsSubmitting(true);
    try {
      const tokens = await authApi.login(credentials);
      tokenStorage.setTokens(tokens.access_token, tokens.refresh_token);
      const me = await authApi.me();
      setUser(me);
    } catch (error) {
      throw toApiError(error);
    } finally {
      setIsSubmitting(false);
    }
  }, []);

  const logout = useCallback(async () => {
    const refreshToken = tokenStorage.getRefreshToken();
    try {
      if (refreshToken) {
        await authApi.logout(refreshToken);
      }
    } catch {
      /* best-effort logout */
    } finally {
      tokenStorage.clear();
      setUser(null);
    }
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: user !== null,
      isInitializing,
      isSubmitting,
      login,
      logout,
      refreshCurrentUser,
    }),
    [user, isInitializing, isSubmitting, login, logout, refreshCurrentUser],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
```

### frontend/src/features/auth/useAuth.ts

```ts
import { useContext } from "react";

import { AuthContext, type AuthContextValue } from "./AuthContext";

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
```

### frontend/src/providers/ThemeProvider.tsx

```tsx
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { storage } from "@/lib/storage";

export type Theme = "light" | "dark" | "system";

interface ThemeContextValue {
  readonly theme: Theme;
  readonly resolvedTheme: "light" | "dark";
  readonly setTheme: (theme: Theme) => void;
  readonly toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

const STORAGE_KEY = "ui.theme";

function getSystemTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

interface ThemeProviderProps {
  readonly children: React.ReactNode;
  readonly defaultTheme?: Theme;
}

export function ThemeProvider({
  children,
  defaultTheme = "system",
}: ThemeProviderProps) {
  const [theme, setThemeState] = useState<Theme>(() => {
    const stored = storage.get<Theme>(STORAGE_KEY);
    return stored ?? defaultTheme;
  });
  const [systemTheme, setSystemTheme] = useState<"light" | "dark">(
    getSystemTheme,
  );

  useEffect(() => {
    const mql = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (event: MediaQueryListEvent) =>
      setSystemTheme(event.matches ? "dark" : "light");
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, []);

  const resolvedTheme: "light" | "dark" =
    theme === "system" ? systemTheme : theme;

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove("light", "dark");
    root.classList.add(resolvedTheme);
  }, [resolvedTheme]);

  const setTheme = useCallback((next: Theme) => {
    setThemeState(next);
    storage.set(STORAGE_KEY, next);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme(resolvedTheme === "dark" ? "light" : "dark");
  }, [resolvedTheme, setTheme]);

  const value = useMemo<ThemeContextValue>(
    () => ({ theme, resolvedTheme, setTheme, toggleTheme }),
    [theme, resolvedTheme, setTheme, toggleTheme],
  );

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within a ThemeProvider");
  return ctx;
}
```

### frontend/src/providers/ToastProvider.tsx

```tsx
import { createContext, useCallback, useContext, useMemo, useState } from "react";

import { cn } from "@/lib/utils";

export type ToastVariant = "default" | "success" | "error";

export interface Toast {
  readonly id: string;
  readonly title?: string;
  readonly description?: string;
  readonly variant: ToastVariant;
}

interface ToastContextValue {
  readonly toast: (input: Omit<Toast, "id" | "variant"> & { variant?: ToastVariant }) => void;
  readonly dismiss: (id: string) => void;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

interface ToastProviderProps {
  readonly children: React.ReactNode;
}

const AUTO_DISMISS_MS = 4500;

export function ToastProvider({ children }: ToastProviderProps) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const dismiss = useCallback((id: string) => {
    setToasts((current) => current.filter((t) => t.id !== id));
  }, []);

  const toast = useCallback<ToastContextValue["toast"]>(
    (input) => {
      const id = crypto.randomUUID();
      const next: Toast = {
        id,
        title: input.title,
        description: input.description,
        variant: input.variant ?? "default",
      };
      setToasts((current) => [...current, next]);
      window.setTimeout(() => dismiss(id), AUTO_DISMISS_MS);
    },
    [dismiss],
  );

  const value = useMemo<ToastContextValue>(
    () => ({ toast, dismiss }),
    [toast, dismiss],
  );

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div
        aria-live="polite"
        className="pointer-events-none fixed inset-x-0 top-0 z-[100] flex flex-col items-center gap-2 p-4 sm:items-end"
      >
        {toasts.map((t) => (
          <div
            key={t.id}
            role="status"
            className={cn(
              "pointer-events-auto w-full max-w-sm rounded-md border p-4 shadow-lg backdrop-blur",
              t.variant === "success" &&
                "border-emerald-500/40 bg-emerald-500/10 text-emerald-900 dark:text-emerald-100",
              t.variant === "error" &&
                "border-destructive/40 bg-destructive/10 text-destructive",
              t.variant === "default" &&
                "border-border bg-card text-card-foreground",
            )}
          >
            {t.title && <p className="text-sm font-medium">{t.title}</p>}
            {t.description && (
              <p className="mt-1 text-sm opacity-90">{t.description}</p>
            )}
            <button
              type="button"
              onClick={() => dismiss(t.id)}
              className="mt-2 text-xs font-medium underline-offset-2 hover:underline"
            >
              Dismiss
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within a ToastProvider");
  return ctx;
}
```

### frontend/src/components/ui/Button.tsx

```tsx
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { forwardRef, type ButtonHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 py-2",
        lg: "h-11 px-6",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  },
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  readonly asChild?: boolean;
  readonly isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      asChild = false,
      isLoading = false,
      disabled,
      children,
      ...props
    },
    ref,
  ) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <span
            aria-hidden="true"
            className="h-4 w-4 animate-spin rounded-full border-2 border-current border-r-transparent"
          />
        ) : null}
        {children}
      </Comp>
    );
  },
);
Button.displayName = "Button";
```

### frontend/src/components/ui/Input.tsx

```tsx
import { forwardRef, type InputHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export type InputProps = InputHTMLAttributes<HTMLInputElement>;

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", ...props }, ref) => (
    <input
      ref={ref}
      type={type}
      className={cn(
        "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background",
        "file:border-0 file:bg-transparent file:text-sm file:font-medium",
        "placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";
```

### frontend/src/components/ui/Label.tsx

```tsx
import { forwardRef, type LabelHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export type LabelProps = LabelHTMLAttributes<HTMLLabelElement>;

export const Label = forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, ...props }, ref) => (
    <label
      ref={ref}
      className={cn(
        "text-sm font-medium leading-none text-foreground",
        "peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
        className,
      )}
      {...props}
    />
  ),
);
Label.displayName = "Label";
```

### frontend/src/components/ui/Card.tsx

```tsx
import { forwardRef, type HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-lg border border-border bg-card text-card-foreground shadow-sm",
        className,
      )}
      {...props}
    />
  ),
);
Card.displayName = "Card";

export const CardHeader = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

export const CardTitle = forwardRef<
  HTMLHeadingElement,
  HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-lg font-semibold leading-none tracking-tight",
      className,
    )}
    {...props}
  />
));
CardTitle.displayName = "CardTitle";

export const CardDescription = forwardRef<
  HTMLParagraphElement,
  HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

export const CardContent = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
));
CardContent.displayName = "CardContent";

export const CardFooter = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";
```

### frontend/src/components/ui/Spinner.tsx

```tsx
import { cn } from "@/lib/utils";

interface SpinnerProps {
  readonly className?: string;
  readonly label?: string;
}

export function Spinner({ className, label = "Loading" }: SpinnerProps) {
  return (
    <span role="status" aria-label={label} className={cn("inline-flex", className)}>
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-current border-r-transparent" />
      <span className="sr-only">{label}</span>
    </span>
  );
}
```

### frontend/src/components/ui/PageLoader.tsx

```tsx
import { Spinner } from "./Spinner";

export function PageLoader() {
  return (
    <div className="flex h-full min-h-[60vh] w-full items-center justify-center">
      <Spinner className="text-muted-foreground" />
    </div>
  );
}
```

### frontend/src/components/ui/EmptyState.tsx

```tsx
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface EmptyStateProps {
  readonly title: string;
  readonly description?: string;
  readonly action?: ReactNode;
  readonly className?: string;
}

export function EmptyState({
  title,
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-lg border border-dashed border-border bg-card p-10 text-center",
        className,
      )}
    >
      <h3 className="text-lg font-semibold">{title}</h3>
      {description && (
        <p className="mt-2 max-w-md text-sm text-muted-foreground">
          {description}
        </p>
      )}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}
```

### frontend/src/components/layout/Sidebar.tsx

```tsx
import { NavLink } from "react-router-dom";

import {
  PRIMARY_NAVIGATION,
  SECONDARY_NAVIGATION,
  type NavigationItem,
} from "@/config/navigation";
import { ENV } from "@/config/env";
import { cn } from "@/lib/utils";

interface SidebarProps {
  readonly isOpen: boolean;
  readonly onClose: () => void;
}

function NavItem({ item }: { item: NavigationItem }) {
  const Icon = item.icon;
  return (
    <NavLink
      to={item.path}
      className={({ isActive }) =>
        cn(
          "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
          isActive
            ? "bg-primary text-primary-foreground"
            : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
        )
      }
    >
      <Icon className="h-4 w-4" aria-hidden="true" />
      <span className="truncate">{item.label}</span>
    </NavLink>
  );
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  return (
    <>
      {isOpen && (
        <div
          role="presentation"
          onClick={onClose}
          className="fixed inset-0 z-30 bg-background/60 backdrop-blur-sm md:hidden"
        />
      )}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-border bg-card transition-transform duration-200 md:sticky md:top-0 md:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-16 shrink-0 items-center gap-2 border-b border-border px-4">
          <span className="text-sm font-semibold uppercase tracking-widest text-primary">
            SBOT
          </span>
          <span className="truncate text-sm text-muted-foreground">
            {ENV.APP_NAME}
          </span>
        </div>
        <nav className="flex-1 overflow-y-auto px-3 py-4">
          <div className="space-y-1">
            {PRIMARY_NAVIGATION.map((item) => (
              <NavItem key={item.path} item={item} />
            ))}
          </div>
          <div className="mt-8 space-y-1">
            <p className="px-3 pb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Account
            </p>
            {SECONDARY_NAVIGATION.map((item) => (
              <NavItem key={item.path} item={item} />
            ))}
          </div>
        </nav>
      </aside>
    </>
  );
}
```

### frontend/src/components/layout/Topbar.tsx

```tsx
import { LogOut, Menu, Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { useAuth } from "@/features/auth/useAuth";
import { useTheme } from "@/providers/ThemeProvider";

interface TopbarProps {
  readonly onOpenSidebar: () => void;
}

function initials(name: string): string {
  return name
    .split(/\s+/)
    .map((part) => part[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export function Topbar({ onOpenSidebar }: TopbarProps) {
  const { user, logout } = useAuth();
  const { resolvedTheme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between gap-4 border-b border-border bg-background/95 px-4 backdrop-blur">
      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={onOpenSidebar}
          aria-label="Open sidebar"
        >
          <Menu className="h-5 w-5" />
        </Button>
        <div className="hidden md:block">
          <h1 className="text-sm font-semibold">Sprint Outcome Tracer</h1>
          <p className="text-xs text-muted-foreground">
            Trace engineering work to business outcomes
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          aria-label="Toggle theme"
        >
          {resolvedTheme === "dark" ? (
            <Sun className="h-4 w-4" />
          ) : (
            <Moon className="h-4 w-4" />
          )}
        </Button>

        {user && (
          <div className="flex items-center gap-3 rounded-md border border-border bg-card px-3 py-1.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground">
              {initials(user.full_name)}
            </div>
            <div className="hidden sm:block">
              <p className="text-sm font-medium leading-none">{user.full_name}</p>
              <p className="text-xs text-muted-foreground">{user.email}</p>
            </div>
          </div>
        )}

        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => void logout()}
        >
          <LogOut className="h-4 w-4" />
          <span className="hidden sm:inline">Log out</span>
        </Button>
      </div>
    </header>
  );
}
```

### frontend/src/components/layout/AppLayout.tsx

```tsx
import { useState } from "react";
import { Outlet } from "react-router-dom";

import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function AppLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  return (
    <div className="flex min-h-screen w-full bg-background">
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar onOpenSidebar={() => setIsSidebarOpen(true)} />
        <main className="flex-1 overflow-x-hidden">
          <div className="container mx-auto max-w-7xl px-4 py-6 md:px-6 md:py-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
```

### frontend/src/router/ProtectedRoute.tsx

```tsx
import { Navigate, useLocation } from "react-router-dom";

import { PageLoader } from "@/components/ui/PageLoader";
import { ROUTES } from "@/config/routes";
import { useAuth } from "@/features/auth/useAuth";

interface ProtectedRouteProps {
  readonly children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isInitializing } = useAuth();
  const location = useLocation();

  if (isInitializing) {
    return <PageLoader />;
  }

  if (!isAuthenticated) {
    return (
      <Navigate
        to={ROUTES.LOGIN}
        replace
        state={{ from: `${location.pathname}${location.search}` }}
      />
    );
  }

  return <>{children}</>;
}
```

### frontend/src/router/PublicRoute.tsx

```tsx
import { Navigate } from "react-router-dom";

import { PageLoader } from "@/components/ui/PageLoader";
import { ROUTES } from "@/config/routes";
import { useAuth } from "@/features/auth/useAuth";

interface PublicRouteProps {
  readonly children: React.ReactNode;
}

export function PublicRoute({ children }: PublicRouteProps) {
  const { isAuthenticated, isInitializing } = useAuth();

  if (isInitializing) {
    return <PageLoader />;
  }

  if (isAuthenticated) {
    return <Navigate to={ROUTES.DASHBOARD} replace />;
  }

  return <>{children}</>;
}
```

### frontend/src/router/AppRouter.tsx

```tsx
import { Suspense, lazy } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "@/components/layout/AppLayout";
import { PageLoader } from "@/components/ui/PageLoader";
import { ROUTES } from "@/config/routes";

import { ProtectedRoute } from "./ProtectedRoute";
import { PublicRoute } from "./PublicRoute";

const LoginPage = lazy(() => import("@/pages/auth/LoginPage"));
const DashboardPage = lazy(() => import("@/pages/dashboard/DashboardPage"));
const NotFoundPage = lazy(() => import("@/pages/NotFoundPage"));
const ModulePlaceholder = lazy(() => import("@/pages/ModulePlaceholder"));

export function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route
            path={ROUTES.ROOT}
            element={<Navigate to={ROUTES.DASHBOARD} replace />}
          />

          <Route
            path={ROUTES.LOGIN}
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />

          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
            <Route
              path={ROUTES.ORGANIZATIONS}
              element={<ModulePlaceholder title="Organizations" />}
            />
            <Route
              path={ROUTES.TEAMS}
              element={<ModulePlaceholder title="Teams" />}
            />
            <Route
              path={ROUTES.USERS}
              element={<ModulePlaceholder title="Users" />}
            />
            <Route
              path={ROUTES.PROJECTS}
              element={<ModulePlaceholder title="Projects" />}
            />
            <Route
              path={ROUTES.SPRINTS}
              element={<ModulePlaceholder title="Sprints" />}
            />
            <Route
              path={ROUTES.WORK_ITEMS}
              element={<ModulePlaceholder title="Work Items" />}
            />
            <Route
              path={ROUTES.BUSINESS_OUTCOMES}
              element={<ModulePlaceholder title="Business Outcomes" />}
            />
            <Route
              path={ROUTES.KPIS}
              element={<ModulePlaceholder title="KPIs" />}
            />
            <Route
              path={ROUTES.OKRS}
              element={<ModulePlaceholder title="OKRs" />}
            />
            <Route
              path={ROUTES.REPORTS}
              element={<ModulePlaceholder title="Reports" />}
            />
            <Route
              path={ROUTES.PROFILE}
              element={<ModulePlaceholder title="Profile" />}
            />
          </Route>

          <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

### frontend/src/pages/auth/LoginPage.tsx

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useForm } from "react-hook-form";
import { useLocation, useNavigate } from "react-router-dom";
import { z } from "zod";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { ENV } from "@/config/env";
import { ROUTES } from "@/config/routes";
import { useAuth } from "@/features/auth/useAuth";
import { useToast } from "@/providers/ToastProvider";

const loginSchema = z.object({
  email: z
    .string()
    .min(1, "Email is required")
    .email("Enter a valid email address"),
  password: z.string().min(1, "Password is required"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

interface LocationState {
  readonly from?: string;
}

export default function LoginPage() {
  const { login, isSubmitting } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();
  const redirectTo =
    (location.state as LocationState | null)?.from ?? ROUTES.DASHBOARD;

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  const onSubmit = handleSubmit(async (values) => {
    try {
      await login(values);
      toast({ title: "Welcome back", variant: "success" });
      navigate(redirectTo, { replace: true });
    } catch (error) {
      const err = toApiError(error);
      toast({
        title: "Sign-in failed",
        description: err.message,
        variant: "error",
      });
    }
  });

  const submitting = isSubmitting || formSubmitting;

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-background px-4 py-10">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-2 text-center">
          <p className="text-xs font-semibold uppercase tracking-widest text-primary">
            {ENV.APP_NAME}
          </p>
          <CardTitle>Sign in</CardTitle>
          <CardDescription>
            Access sprints, outcomes, and KPIs in one place.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={onSubmit} className="space-y-4" noValidate>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                autoComplete="email"
                placeholder="you@company.com"
                aria-invalid={Boolean(errors.email)}
                {...register("email")}
              />
              {errors.email && (
                <p className="text-xs text-destructive">
                  {errors.email.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                placeholder="••••••••"
                aria-invalid={Boolean(errors.password)}
                {...register("password")}
              />
              {errors.password && (
                <p className="text-xs text-destructive">
                  {errors.password.message}
                </p>
              )}
            </div>

            <Button type="submit" className="w-full" disabled={submitting}>
              {submitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Signing in...
                </>
              ) : (
                "Sign in"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
```

### frontend/src/pages/dashboard/DashboardPage.tsx

```tsx
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/Card";
import { useAuth } from "@/features/auth/useAuth";

const STATS: ReadonlyArray<{
  label: string;
  value: string;
  description: string;
}> = [
  {
    label: "Active Sprints",
    value: "—",
    description: "Sprints currently in progress",
  },
  {
    label: "Outcomes On Track",
    value: "—",
    description: "Business outcomes with healthy progress",
  },
  {
    label: "KPIs Monitored",
    value: "—",
    description: "Metrics under active tracking",
  },
  {
    label: "Attribution Coverage",
    value: "—",
    description: "Completed work items linked to outcomes",
  },
];

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">
          Welcome{user ? `, ${user.full_name.split(" ")[0]}` : ""}.
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Your organization's business outcome tracker.
        </p>
      </header>

      <section
        aria-label="Key metrics"
        className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"
      >
        {STATS.map((stat) => (
          <Card key={stat.label}>
            <CardHeader className="pb-2">
              <CardDescription className="text-xs uppercase tracking-wide">
                {stat.label}
              </CardDescription>
              <CardTitle className="text-3xl">{stat.value}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Sprints</CardTitle>
            <CardDescription>
              Sprint activity across your projects will appear here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Once modules are enabled, this panel will summarize sprint
              velocity, completion rate, and outcome attribution.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Outcomes At Risk</CardTitle>
            <CardDescription>
              Outcomes flagged as at risk or off track will be listed here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Progress vs. time-elapsed will drive automated risk detection
              once outcomes and KPIs are populated.
            </p>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
```

### frontend/src/pages/NotFoundPage.tsx

```tsx
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/Button";
import { ROUTES } from "@/config/routes";

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen w-full flex-col items-center justify-center bg-background px-4 text-center">
      <p className="text-sm font-semibold uppercase tracking-widest text-primary">
        404
      </p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">
        Page not found
      </h1>
      <p className="mt-2 max-w-md text-sm text-muted-foreground">
        The page you were looking for doesn't exist, was moved, or is not yet
        available.
      </p>
      <Button asChild className="mt-6">
        <Link to={ROUTES.DASHBOARD}>Back to dashboard</Link>
      </Button>
    </div>
  );
}
```

### frontend/src/pages/ModulePlaceholder.tsx

```tsx
import { Sparkles } from "lucide-react";

import { EmptyState } from "@/components/ui/EmptyState";

interface ModulePlaceholderProps {
  readonly title: string;
  readonly description?: string;
}

export default function ModulePlaceholder({
  title,
  description,
}: ModulePlaceholderProps) {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          This module is part of the Sprint Business Outcome Tracer roadmap.
        </p>
      </header>

      <EmptyState
        title={`${title} is coming soon`}
        description={
          description ??
          "The foundation is in place. Feature screens for this module will be enabled in an upcoming release."
        }
        action={
          <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
            <Sparkles className="h-4 w-4 text-primary" />
            <span>Under active development</span>
          </div>
        }
      />
    </div>
  );
}
```

### frontend/src/vite-env.d.ts

```ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string;
  readonly VITE_APP_NAME?: string;
  readonly VITE_STORAGE_PREFIX?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

### frontend/.gitignore

```gitignore
node_modules
dist
dist-ssr
.env
.env.*
!.env.example
.DS_Store
*.log
.vscode
.idea
```

### frontend/README.md

```markdown
# Sprint Business Outcome Tracer — Frontend

React 18 + Vite + TypeScript + TailwindCSS + shadcn/ui foundation for the
Sprint Business Outcome Tracer.

## Quick start

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The dev server proxies `/api` to the backend at `http://localhost:8000`.

## Scripts

- `npm run dev` — start the Vite dev server
- `npm run build` — type-check and build the production bundle
- `npm run preview` — preview the production build
- `npm run lint` — run ESLint

## Project structure

- `src/api` — Axios client, endpoints, error mapping
- `src/components/layout` — `AppLayout`, `Sidebar`, `Topbar`
- `src/components/ui` — reusable primitives (`Button`, `Input`, `Card`, ...)
- `src/config` — environment, routes, navigation
- `src/features/auth` — auth provider, hook, API, types
- `src/lib` — utilities (`cn`, `storage`, `tokens`)
- `src/pages` — top-level pages (login, dashboard, 404, placeholder)
- `src/providers` — `ThemeProvider`, `ToastProvider`
- `src/router` — `AppRouter`, `ProtectedRoute`, `PublicRoute`

## Notes

- All routes are registered in `src/router/AppRouter.tsx` using the `ROUTES`
  constants from `src/config/routes.ts`.
- Routes for modules that are not yet implemented render `ModulePlaceholder`.
- `AuthProvider` wraps the app and handles token storage, refresh, and the
  current user.
```

================================================================================

### frontend/src/features/projects/types.ts

```ts
export interface Project {
  readonly id: string;
  readonly organization_id: string;
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly description: string | null;
  readonly start_date: string | null;
  readonly target_end_date: string | null;
  readonly is_archived: boolean;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface Team {
  readonly id: string;
  readonly organization_id: string;
  readonly name: string;
  readonly slug: string;
  readonly description: string | null;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface CreateProjectInput {
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly description?: string | null;
  readonly start_date?: string | null;
  readonly target_end_date?: string | null;
}

export interface UpdateProjectInput {
  readonly name?: string;
  readonly description?: string | null;
  readonly start_date?: string | null;
  readonly target_end_date?: string | null;
  readonly is_archived?: boolean;
}

export interface PaginatedProjects {
  readonly items: Project[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedTeams {
  readonly items: Team[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface ProjectListParams {
  readonly limit: number;
  readonly offset: number;
  readonly team_id?: string;
  readonly include_archived?: boolean;
}
```

### frontend/src/features/projects/projectsApi.ts

```ts
import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CreateProjectInput,
  PaginatedProjects,
  PaginatedTeams,
  Project,
  ProjectListParams,
  UpdateProjectInput,
} from "./types";

export const projectsApi = {
  async list(params: ProjectListParams): Promise<PaginatedProjects> {
    const query: Record<string, string | number | boolean> = {
      limit: params.limit,
      offset: params.offset,
      include_archived: params.include_archived ?? false,
    };
    if (params.team_id) {
      query.team_id = params.team_id;
    }
    const response = await apiClient.get<PaginatedProjects>(
      API_ENDPOINTS.PROJECTS,
      { params: query },
    );
    return response.data;
  },

  async get(id: string): Promise<Project> {
    const response = await apiClient.get<Project>(
      `${API_ENDPOINTS.PROJECTS}/${id}`,
    );
    return response.data;
  },

  async create(input: CreateProjectInput): Promise<Project> {
    const response = await apiClient.post<Project>(
      API_ENDPOINTS.PROJECTS,
      input,
    );
    return response.data;
  },

  async update(id: string, input: UpdateProjectInput): Promise<Project> {
    const response = await apiClient.patch<Project>(
      `${API_ENDPOINTS.PROJECTS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.PROJECTS}/${id}`);
  },

  async listTeams(): Promise<PaginatedTeams> {
    const response = await apiClient.get<PaginatedTeams>(API_ENDPOINTS.TEAMS, {
      params: { limit: 200, offset: 0 },
    });
    return response.data;
  },
};
```

### frontend/src/features/projects/projectSchemas.ts

```ts
import { z } from "zod";

const slugRegex = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const keyRegex = /^[A-Z0-9]+$/;

const optionalDate = z
  .string()
  .trim()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "Use YYYY-MM-DD")
  .optional()
  .or(z.literal(""));

export const createProjectSchema = z
  .object({
    team_id: z.string().uuid("Select a team"),
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    key: z
      .string()
      .trim()
      .min(2, "Key must be between 2 and 12 characters")
      .max(12, "Key must be between 2 and 12 characters")
      .regex(keyRegex, "Key must be uppercase alphanumeric")
      .transform((v) => v.toUpperCase()),
    slug: z
      .string()
      .trim()
      .min(2, "Slug must be between 2 and 64 characters")
      .max(64, "Slug must be between 2 and 64 characters")
      .regex(
        slugRegex,
        "Slug must be lowercase alphanumeric with hyphens",
      ),
    description: z
      .string()
      .trim()
      .max(2000, "Description must be 2000 characters or fewer")
      .optional()
      .or(z.literal("")),
    start_date: optionalDate,
    target_end_date: optionalDate,
  })
  .superRefine((values, ctx) => {
    if (values.start_date && values.target_end_date) {
      if (values.target_end_date < values.start_date) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Target end date cannot be before start date",
          path: ["target_end_date"],
        });
      }
    }
  });

export type CreateProjectFormValues = z.infer<typeof createProjectSchema>;

export const editProjectSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    description: z
      .string()
      .trim()
      .max(2000, "Description must be 2000 characters or fewer")
      .optional()
      .or(z.literal("")),
    start_date: optionalDate,
    target_end_date: optionalDate,
    is_archived: z.boolean(),
  })
  .superRefine((values, ctx) => {
    if (values.start_date && values.target_end_date) {
      if (values.target_end_date < values.start_date) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Target end date cannot be before start date",
          path: ["target_end_date"],
        });
      }
    }
  });

export type EditProjectFormValues = z.infer<typeof editProjectSchema>;
```

### frontend/src/features/projects/useProjects.ts

```ts
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { toApiError, ApiError } from "@/api/errors";

import { projectsApi } from "./projectsApi";
import type {
  CreateProjectInput,
  PaginatedProjects,
  Project,
  ProjectListParams,
  UpdateProjectInput,
} from "./types";

interface UseProjectsOptions {
  readonly limit: number;
}

interface UseProjectsResult {
  readonly data: PaginatedProjects | null;
  readonly filtered: Project[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly search: string;
  readonly includeArchived: boolean;
  readonly setSearch: (value: string) => void;
  readonly setIncludeArchived: (value: boolean) => void;
  readonly setPage: (page: number) => void;
  readonly refresh: () => Promise<void>;
  readonly createProject: (input: CreateProjectInput) => Promise<Project>;
  readonly updateProject: (
    id: string,
    input: UpdateProjectInput,
  ) => Promise<Project>;
  readonly deleteProject: (id: string) => Promise<void>;
}

export function useProjects(
  options: UseProjectsOptions = { limit: 20 },
): UseProjectsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedProjects | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [search, setSearch] = useState<string>("");
  const [includeArchived, setIncludeArchived] = useState<boolean>(false);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, archived: boolean) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: ProjectListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
          include_archived: archived,
        };
        const result = await projectsApi.list(params);
        if (!mounted.current) return;
        setData(result);
      } catch (err) {
        if (!mounted.current) return;
        setError(toApiError(err));
      } finally {
        if (mounted.current) setIsLoading(false);
      }
    },
    [limit],
  );

  useEffect(() => {
    mounted.current = true;
    void load(page, includeArchived);
    return () => {
      mounted.current = false;
    };
  }, [load, page, includeArchived]);

  const refresh = useCallback(async () => {
    await load(page, includeArchived);
  }, [load, page, includeArchived]);

  const createProject = useCallback(
    async (input: CreateProjectInput) => {
      setIsMutating(true);
      try {
        const created = await projectsApi.create(input);
        await load(1, includeArchived);
        setPage(1);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load, includeArchived],
  );

  const updateProject = useCallback(
    async (id: string, input: UpdateProjectInput) => {
      setIsMutating(true);
      try {
        const updated = await projectsApi.update(id, input);
        await load(page, includeArchived);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, includeArchived],
  );

  const deleteProject = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await projectsApi.remove(id);
        const remaining = (data?.items.length ?? 1) - 1;
        const nextPage = remaining <= 0 && page > 1 ? page - 1 : page;
        if (nextPage !== page) {
          setPage(nextPage);
        } else {
          await load(nextPage, includeArchived);
        }
      } finally {
        setIsMutating(false);
      }
    },
    [data, load, page, includeArchived],
  );

  const filtered = useMemo(() => {
    if (!data) return [];
    const term = search.trim().toLowerCase();
    if (!term) return data.items;
    return data.items.filter((project) => {
      return (
        project.name.toLowerCase().includes(term) ||
        project.key.toLowerCase().includes(term) ||
        project.slug.toLowerCase().includes(term) ||
        (project.description ?? "").toLowerCase().includes(term)
      );
    });
  }, [data, search]);

  const totalPages = data ? Math.max(1, Math.ceil(data.total / limit)) : 1;

  return {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    search,
    includeArchived,
    setSearch,
    setIncludeArchived,
    setPage,
    refresh,
    createProject,
    updateProject,
    deleteProject,
  };
}
```

### frontend/src/features/projects/useTeams.ts

```ts
import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { projectsApi } from "./projectsApi";
import type { Team } from "./types";

interface UseTeamsResult {
  readonly teams: Team[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useTeams(): UseTeamsResult {
  const [teams, setTeams] = useState<Team[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await projectsApi.listTeams();
        if (!cancelled) setTeams(result.items);
      } catch (err) {
        if (!cancelled) setError(toApiError(err));
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return { teams, isLoading, error };
}
```

### frontend/src/features/projects/components/ProjectStatusBadge.tsx

```tsx
import { cn } from "@/lib/utils";

interface ProjectStatusBadgeProps {
  readonly isArchived: boolean;
}

export function ProjectStatusBadge({ isArchived }: ProjectStatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        isArchived
          ? "border border-border bg-muted text-muted-foreground"
          : "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
      )}
    >
      {isArchived ? "Archived" : "Active"}
    </span>
  );
}
```

### frontend/src/features/projects/components/ProjectSearch.tsx

```tsx
import { Search } from "lucide-react";

import { Input } from "@/components/ui/Input";

interface ProjectSearchProps {
  readonly value: string;
  readonly onChange: (value: string) => void;
  readonly includeArchived: boolean;
  readonly onIncludeArchivedChange: (value: boolean) => void;
}

export function ProjectSearch({
  value,
  onChange,
  includeArchived,
  onIncludeArchivedChange,
}: ProjectSearchProps) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="relative w-full sm:max-w-sm">
        <Search
          aria-hidden="true"
          className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
        />
        <Input
          type="search"
          placeholder="Search by name, key, slug…"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          className="pl-9"
          aria-label="Search projects"
        />
      </div>

      <label className="inline-flex items-center gap-2 text-sm text-muted-foreground">
        <input
          type="checkbox"
          checked={includeArchived}
          onChange={(event) => onIncludeArchivedChange(event.target.checked)}
          className="h-4 w-4 rounded border-input text-primary focus:ring-2 focus:ring-ring"
        />
        Include archived
      </label>
    </div>
  );
}
```

### frontend/src/features/projects/components/Pagination.tsx

```tsx
import { ChevronLeft, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/Button";

interface PaginationProps {
  readonly page: number;
  readonly totalPages: number;
  readonly total: number;
  readonly onChange: (page: number) => void;
}

export function Pagination({
  page,
  totalPages,
  total,
  onChange,
}: PaginationProps) {
  const canPrev = page > 1;
  const canNext = page < totalPages;

  return (
    <div className="flex flex-col items-center justify-between gap-3 border-t border-border pt-4 text-sm text-muted-foreground sm:flex-row">
      <p>
        Page <span className="font-medium text-foreground">{page}</span> of{" "}
        <span className="font-medium text-foreground">{totalPages}</span>
        <span className="mx-2 opacity-50">•</span>
        <span>{total} total</span>
      </p>
      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => onChange(page - 1)}
          disabled={!canPrev}
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </Button>
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => onChange(page + 1)}
          disabled={!canNext}
        >
          Next
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
```

### frontend/src/features/projects/components/ProjectsTable.tsx

```tsx
import { Archive, ArchiveRestore, Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type { Project } from "../types";
import { ProjectStatusBadge } from "./ProjectStatusBadge";

interface ProjectsTableProps {
  readonly projects: Project[];
  readonly onEdit: (project: Project) => void;
  readonly onDelete: (project: Project) => void;
  readonly onToggleArchive: (project: Project) => void;
  readonly isMutating: boolean;
}

function formatDate(value: string | null): string {
  if (!value) return "—";
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) return value;
  return new Date(parsed).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });
}

export function ProjectsTable({
  projects,
  onEdit,
  onDelete,
  onToggleArchive,
  isMutating,
}: ProjectsTableProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Key
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Name
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Start
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Target End
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {projects.map((project) => (
              <tr
                key={project.id}
                className={cn(
                  "transition-colors hover:bg-muted/30",
                  project.is_archived && "opacity-70",
                )}
              >
                <td className="px-4 py-3 font-mono text-xs font-semibold text-foreground">
                  {project.key}
                </td>
                <td className="px-4 py-3">
                  <div className="flex flex-col">
                    <span className="font-medium text-foreground">
                      {project.name}
                    </span>
                    {project.description && (
                      <span className="line-clamp-1 text-xs text-muted-foreground">
                        {project.description}
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-4 py-3">
                  <ProjectStatusBadge isArchived={project.is_archived} />
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {formatDate(project.start_date)}
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {formatDate(project.target_end_date)}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Edit ${project.name}`}
                      onClick={() => onEdit(project)}
                      disabled={isMutating}
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={
                        project.is_archived
                          ? `Restore ${project.name}`
                          : `Archive ${project.name}`
                      }
                      onClick={() => onToggleArchive(project)}
                      disabled={isMutating}
                    >
                      {project.is_archived ? (
                        <ArchiveRestore className="h-4 w-4" />
                      ) : (
                        <Archive className="h-4 w-4" />
                      )}
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Delete ${project.name}`}
                      onClick={() => onDelete(project)}
                      disabled={isMutating}
                      className="text-destructive hover:bg-destructive/10 hover:text-destructive"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

### frontend/src/features/projects/components/Modal.tsx

```tsx
import { X } from "lucide-react";
import { useEffect } from "react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

interface ModalProps {
  readonly open: boolean;
  readonly title: string;
  readonly description?: string;
  readonly onClose: () => void;
  readonly children: React.ReactNode;
  readonly maxWidthClassName?: string;
}

export function Modal({
  open,
  title,
  description,
  onClose,
  children,
  maxWidthClassName = "max-w-lg",
}: ModalProps) {
  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={title}
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <div
        role="presentation"
        onClick={onClose}
        className="absolute inset-0 bg-background/70 backdrop-blur-sm"
      />
      <div
        className={cn(
          "relative w-full rounded-lg border border-border bg-card p-6 shadow-lg",
          maxWidthClassName,
        )}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold">{title}</h2>
            {description && (
              <p className="mt-1 text-sm text-muted-foreground">
                {description}
              </p>
            )}
          </div>
          <Button
            type="button"
            variant="ghost"
            size="icon"
            aria-label="Close dialog"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
}
```

### frontend/src/features/projects/components/CreateProjectDialog.tsx

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import { useTeams } from "../useTeams";
import {
  createProjectSchema,
  type CreateProjectFormValues,
} from "../projectSchemas";
import type { CreateProjectInput } from "../types";
import { Modal } from "./Modal";

interface CreateProjectDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateProjectInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 64);
}

function keyify(value: string): string {
  return value
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, "")
    .slice(0, 12);
}

export function CreateProjectDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
}: CreateProjectDialogProps) {
  const { teams, isLoading: teamsLoading, error: teamsError } = useTeams();
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateProjectFormValues>({
    resolver: zodResolver(createProjectSchema),
    defaultValues: {
      team_id: "",
      name: "",
      key: "",
      slug: "",
      description: "",
      start_date: "",
      target_end_date: "",
    },
  });

  useEffect(() => {
    if (!open) reset();
  }, [open, reset]);

  const nameValue = watch("name");
  const keyValue = watch("key");
  const slugValue = watch("slug");

  useEffect(() => {
    if (!nameValue) return;
    if (!keyValue) {
      setValue("key", keyify(nameValue), { shouldValidate: false });
    }
    if (!slugValue) {
      setValue("slug", slugify(nameValue), { shouldValidate: false });
    }
  }, [nameValue, keyValue, slugValue, setValue]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: CreateProjectInput = {
        team_id: values.team_id,
        name: values.name.trim(),
        key: values.key.trim().toUpperCase(),
        slug: values.slug.trim().toLowerCase(),
        description: values.description ? values.description.trim() : null,
        start_date: values.start_date ? values.start_date : null,
        target_end_date: values.target_end_date ? values.target_end_date : null,
      };
      await onSubmit(input);
      toast({ title: "Project created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create project",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create project"
      description="Projects group sprints, work items, and outcomes."
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="team_id">Team</Label>
          {teamsError && (
            <p className="text-xs text-destructive">{teamsError.message}</p>
          )}
          <select
            id="team_id"
            {...register("team_id")}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            disabled={teamsLoading}
            aria-invalid={Boolean(errors.team_id)}
          >
            <option value="">
              {teamsLoading ? "Loading teams…" : "Select a team"}
            </option>
            {teams.map((team) => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
          {errors.team_id && (
            <p className="text-xs text-destructive">{errors.team_id.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            placeholder="e.g. Sprint Outcome Tracer"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="key">Key</Label>
            <Input
              id="key"
              placeholder="SBOT"
              {...register("key")}
              aria-invalid={Boolean(errors.key)}
            />
            {errors.key && (
              <p className="text-xs text-destructive">{errors.key.message}</p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="slug">Slug</Label>
            <Input
              id="slug"
              placeholder="sprint-outcome-tracer"
              {...register("slug")}
              aria-invalid={Boolean(errors.slug)}
            />
            {errors.slug && (
              <p className="text-xs text-destructive">{errors.slug.message}</p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="description">Description</Label>
          <textarea
            id="description"
            rows={3}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Optional summary of what the project delivers"
            {...register("description")}
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="start_date">Start date</Label>
            <Input
              id="start_date"
              type="date"
              {...register("start_date")}
              aria-invalid={Boolean(errors.start_date)}
            />
            {errors.start_date && (
              <p className="text-xs text-destructive">
                {errors.start_date.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="target_end_date">Target end date</Label>
            <Input
              id="target_end_date"
              type="date"
              {...register("target_end_date")}
              aria-invalid={Boolean(errors.target_end_date)}
            />
            {errors.target_end_date && (
              <p className="text-xs text-destructive">
                {errors.target_end_date.message}
              </p>
            )}
          </div>
        </div>

        <div className="flex items-center justify-end gap-2 pt-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={submitting}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating…
              </>
            ) : (
              "Create project"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
```

### frontend/src/features/projects/components/EditProjectDialog.tsx

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import {
  editProjectSchema,
  type EditProjectFormValues,
} from "../projectSchemas";
import type { Project, UpdateProjectInput } from "../types";
import { Modal } from "./Modal";

interface EditProjectDialogProps {
  readonly open: boolean;
  readonly project: Project | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateProjectInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function EditProjectDialog({
  open,
  project,
  onClose,
  onSubmit,
  isSubmitting,
}: EditProjectDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditProjectFormValues>({
    resolver: zodResolver(editProjectSchema),
    defaultValues: {
      name: "",
      description: "",
      start_date: "",
      target_end_date: "",
      is_archived: false,
    },
  });

  useEffect(() => {
    if (open && project) {
      reset({
        name: project.name,
        description: project.description ?? "",
        start_date: project.start_date ?? "",
        target_end_date: project.target_end_date ?? "",
        is_archived: project.is_archived,
      });
    }
  }, [open, project, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!project) return;
    try {
      const input: UpdateProjectInput = {
        name: values.name.trim(),
        description: values.description ? values.description.trim() : null,
        start_date: values.start_date ? values.start_date : null,
        target_end_date: values.target_end_date ? values.target_end_date : null,
        is_archived: values.is_archived,
      };
      await onSubmit(project.id, input);
      toast({ title: "Project updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update project",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && project !== null}
      onClose={onClose}
      title={`Edit ${project?.name ?? "project"}`}
      description={
        project ? `${project.key} • ${project.slug}` : undefined
      }
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="edit-name">Name</Label>
          <Input
            id="edit-name"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="edit-description">Description</Label>
          <textarea
            id="edit-description"
            rows={3}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            {...register("description")}
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="edit-start">Start date</Label>
            <Input
              id="edit-start"
              type="date"
              {...register("start_date")}
              aria-invalid={Boolean(errors.start_date)}
            />
            {errors.start_date && (
              <p className="text-xs text-destructive">
                {errors.start_date.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-target">Target end date</Label>
            <Input
              id="edit-target"
              type="date"
              {...register("target_end_date")}
              aria-invalid={Boolean(errors.target_end_date)}
            />
            {errors.target_end_date && (
              <p className="text-xs text-destructive">
                {errors.target_end_date.message}
              </p>
            )}
          </div>
        </div>

        <label className="inline-flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-input text-primary focus:ring-2 focus:ring-ring"
            {...register("is_archived")}
          />
          Archived
        </label>

        <div className="flex items-center justify-end gap-2 pt-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={submitting || !isDirty}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Saving…
              </>
            ) : (
              "Save changes"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
```

### frontend/src/features/projects/components/DeleteProjectDialog.tsx

```tsx
import { Loader2, TriangleAlert } from "lucide-react";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { useToast } from "@/providers/ToastProvider";

import type { Project } from "../types";
import { Modal } from "./Modal";

interface DeleteProjectDialogProps {
  readonly open: boolean;
  readonly project: Project | null;
  readonly onClose: () => void;
  readonly onConfirm: (id: string) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function DeleteProjectDialog({
  open,
  project,
  onClose,
  onConfirm,
  isSubmitting,
}: DeleteProjectDialogProps) {
  const { toast } = useToast();

  const handleConfirm = async () => {
    if (!project) return;
    try {
      await onConfirm(project.id);
      toast({ title: "Project deleted", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not delete project",
        description: apiError.message,
        variant: "error",
      });
    }
  };

  return (
    <Modal
      open={open && project !== null}
      onClose={onClose}
      title="Delete project"
      maxWidthClassName="max-w-md"
    >
      <div className="space-y-4">
        <div className="flex items-start gap-3 rounded-md border border-destructive/40 bg-destructive/10 p-3 text-destructive">
          <TriangleAlert className="mt-0.5 h-5 w-5" aria-hidden="true" />
          <div className="text-sm">
            <p className="font-medium">This action cannot be undone.</p>
            <p className="mt-1 opacity-90">
              {project ? (
                <>
                  You are about to permanently remove{" "}
                  <span className="font-semibold">{project.name}</span> (
                  <span className="font-mono">{project.key}</span>).
                </>
              ) : (
                "Project details are unavailable."
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-end gap-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="destructive"
            onClick={() => void handleConfirm()}
            disabled={isSubmitting || !project}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Deleting…
              </>
            ) : (
              "Delete project"
            )}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
```

### frontend/src/features/projects/components/ProjectsErrorState.tsx

```tsx
import { AlertCircle } from "lucide-react";

import { Button } from "@/components/ui/Button";

interface ProjectsErrorStateProps {
  readonly message: string;
  readonly onRetry: () => void;
}

export function ProjectsErrorState({
  message,
  onRetry,
}: ProjectsErrorStateProps) {
  return (
    <div
      role="alert"
      className="flex flex-col items-center justify-center gap-3 rounded-lg border border-destructive/40 bg-destructive/10 p-8 text-center text-destructive"
    >
      <AlertCircle className="h-6 w-6" aria-hidden="true" />
      <div>
        <h3 className="text-base font-semibold">
          Failed to load projects
        </h3>
        <p className="mt-1 text-sm opacity-90">{message}</p>
      </div>
      <Button
        type="button"
        variant="outline"
        onClick={onRetry}
        className="border-destructive/40 text-destructive hover:bg-destructive/20"
      >
        Try again
      </Button>
    </div>
  );
}
```

### frontend/src/features/projects/components/ProjectsLoadingState.tsx

```tsx
export function ProjectsLoadingState() {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="divide-y divide-border">
        {Array.from({ length: 5 }).map((_, index) => (
          <div key={index} className="flex items-center gap-4 p-4">
            <div className="h-4 w-16 animate-pulse rounded bg-muted" />
            <div className="h-4 flex-1 animate-pulse rounded bg-muted" />
            <div className="h-4 w-24 animate-pulse rounded bg-muted" />
            <div className="h-4 w-24 animate-pulse rounded bg-muted" />
            <div className="h-8 w-24 animate-pulse rounded bg-muted" />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### frontend/src/features/projects/index.ts

```ts
export { projectsApi } from "./projectsApi";
export { useProjects } from "./useProjects";
export { useTeams } from "./useTeams";
export type {
  CreateProjectInput,
  PaginatedProjects,
  Project,
  ProjectListParams,
  Team,
  UpdateProjectInput,
} from "./types";
export { CreateProjectDialog } from "./components/CreateProjectDialog";
export { DeleteProjectDialog } from "./components/DeleteProjectDialog";
export { EditProjectDialog } from "./components/EditProjectDialog";
export { Pagination } from "./components/Pagination";
export { ProjectSearch } from "./components/ProjectSearch";
export { ProjectStatusBadge } from "./components/ProjectStatusBadge";
export { ProjectsErrorState } from "./components/ProjectsErrorState";
export { ProjectsLoadingState } from "./components/ProjectsLoadingState";
export { ProjectsTable } from "./components/ProjectsTable";
```

### frontend/src/pages/projects/ProjectsPage.tsx

```tsx
import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CreateProjectDialog,
  DeleteProjectDialog,
  EditProjectDialog,
  Pagination,
  ProjectSearch,
  ProjectsErrorState,
  ProjectsLoadingState,
  ProjectsTable,
  useProjects,
  type Project,
} from "@/features/projects";
import { useToast } from "@/providers/ToastProvider";

const PAGE_SIZE = 20;

export default function ProjectsPage() {
  const {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    search,
    includeArchived,
    setSearch,
    setIncludeArchived,
    setPage,
    refresh,
    createProject,
    updateProject,
    deleteProject,
  } = useProjects({ limit: PAGE_SIZE });
  const { toast } = useToast();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<Project | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Project | null>(null);

  const handleToggleArchive = async (project: Project) => {
    try {
      await updateProject(project.id, { is_archived: !project.is_archived });
      toast({
        title: project.is_archived
          ? "Project restored"
          : "Project archived",
        variant: "success",
      });
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "An unexpected error occurred";
      toast({
        title: "Could not update project",
        description: message,
        variant: "error",
      });
    }
  };

  const hasResults = filtered.length > 0;
  const totalCount = data?.total ?? 0;

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Projects</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage the projects that group sprints, work items, and outcomes.
          </p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          New project
        </Button>
      </header>

      <ProjectSearch
        value={search}
        onChange={setSearch}
        includeArchived={includeArchived}
        onIncludeArchivedChange={(value) => {
          setIncludeArchived(value);
          setPage(1);
        }}
      />

      {isLoading && !data ? (
        <ProjectsLoadingState />
      ) : error ? (
        <ProjectsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            search
              ? "No projects match your search"
              : "No projects yet"
          }
          description={
            search
              ? "Try a different name, key, or slug — or clear the search."
              : "Create your first project to start tracking sprints and outcomes."
          }
          action={
            !search ? (
              <Button type="button" onClick={() => setCreateOpen(true)}>
                <Plus className="h-4 w-4" />
                New project
              </Button>
            ) : (
              <Button
                type="button"
                variant="outline"
                onClick={() => setSearch("")}
              >
                Clear search
              </Button>
            )
          }
        />
      ) : (
        <div className="space-y-4">
          <ProjectsTable
            projects={filtered}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
            onToggleArchive={(project) => void handleToggleArchive(project)}
          />
          <Pagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateProjectDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createProject(input);
        }}
        isSubmitting={isMutating}
      />

      <EditProjectDialog
        open={editTarget !== null}
        project={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateProject(id, input);
        }}
        isSubmitting={isMutating}
      />

      <DeleteProjectDialog
        open={deleteTarget !== null}
        project={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteProject(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
```

---

### MANUAL ROUTER PATCH

Replace the current `ROUTES.PROJECTS` placeholder route inside `src/router/AppRouter.tsx` with a real `ProjectsPage` route.

1. Add this lazy import near the other page imports at the top of `src/router/AppRouter.tsx`:

```tsx
const ProjectsPage = lazy(() => import("@/pages/projects/ProjectsPage"));
```

2. Inside the protected `<Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>` block, replace:

```tsx
<Route
  path={ROUTES.PROJECTS}
  element={<ModulePlaceholder title="Projects" />}
/>
```

with:

```tsx
<Route path={ROUTES.PROJECTS} element={<ProjectsPage />} />
```

No other lines in `AppRouter.tsx` need to change.

================================================================================

### frontend/src/features/sprints/types.ts

```ts
export type SprintStatus =
  | "planned"
  | "active"
  | "completed"
  | "cancelled";

export interface Sprint {
  readonly id: string;
  readonly project_id: string;
  readonly name: string;
  readonly goal: string | null;
  readonly start_date: string;
  readonly end_date: string;
  readonly status: SprintStatus;
  readonly started_at: string | null;
  readonly completed_at: string | null;
  readonly planned_capacity: number;
  readonly completed_points: number;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface SprintProjectOption {
  readonly id: string;
  readonly organization_id: string;
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly is_archived: boolean;
}

export interface PaginatedSprints {
  readonly items: Sprint[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedSprintProjects {
  readonly items: SprintProjectOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface CreateSprintInput {
  readonly project_id: string;
  readonly name: string;
  readonly goal?: string | null;
  readonly start_date: string;
  readonly end_date: string;
  readonly planned_capacity: number;
}

export interface UpdateSprintInput {
  readonly name?: string;
  readonly goal?: string | null;
  readonly start_date?: string;
  readonly end_date?: string;
  readonly planned_capacity?: number;
}

export interface CompleteSprintInput {
  readonly completed_points: number;
}

export interface SprintListParams {
  readonly project_id: string;
  readonly limit: number;
  readonly offset: number;
}
```

### frontend/src/features/sprints/sprintsApi.ts

```ts
import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CompleteSprintInput,
  CreateSprintInput,
  PaginatedSprintProjects,
  PaginatedSprints,
  Sprint,
  SprintListParams,
  UpdateSprintInput,
} from "./types";

export const sprintsApi = {
  async list(params: SprintListParams): Promise<PaginatedSprints> {
    const response = await apiClient.get<PaginatedSprints>(
      API_ENDPOINTS.SPRINTS,
      {
        params: {
          project_id: params.project_id,
          limit: params.limit,
          offset: params.offset,
        },
      },
    );
    return response.data;
  },

  async get(id: string): Promise<Sprint> {
    const response = await apiClient.get<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}`,
    );
    return response.data;
  },

  async create(input: CreateSprintInput): Promise<Sprint> {
    const response = await apiClient.post<Sprint>(
      API_ENDPOINTS.SPRINTS,
      input,
    );
    return response.data;
  },

  async update(id: string, input: UpdateSprintInput): Promise<Sprint> {
    const response = await apiClient.patch<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.SPRINTS}/${id}`);
  },

  async start(id: string): Promise<Sprint> {
    const response = await apiClient.post<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}/start`,
    );
    return response.data;
  },

  async complete(id: string, input: CompleteSprintInput): Promise<Sprint> {
    const response = await apiClient.post<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}/complete`,
      input,
    );
    return response.data;
  },

  async listProjects(): Promise<PaginatedSprintProjects> {
    const response = await apiClient.get<PaginatedSprintProjects>(
      API_ENDPOINTS.PROJECTS,
      {
        params: { limit: 200, offset: 0, include_archived: false },
      },
    );
    return response.data;
  },
};
```

### frontend/src/features/sprints/sprintSchemas.ts

```ts
import { z } from "zod";

const dateString = z
  .string()
  .trim()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "Use YYYY-MM-DD");

const optionalGoal = z
  .string()
  .trim()
  .max(2000, "Goal must be 2000 characters or fewer")
  .optional()
  .or(z.literal(""));

export const createSprintSchema = z
  .object({
    project_id: z.string().uuid("Select a project"),
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    goal: optionalGoal,
    start_date: dateString,
    end_date: dateString,
    planned_capacity: z
      .coerce.number({ invalid_type_error: "Enter a number" })
      .int("Must be a whole number")
      .min(0, "Cannot be negative")
      .max(10000, "Value is too large"),
  })
  .superRefine((values, ctx) => {
    if (values.end_date < values.start_date) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "End date cannot be before start date",
        path: ["end_date"],
      });
    }
  });

export type CreateSprintFormValues = z.infer<typeof createSprintSchema>;

export const editSprintSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    goal: optionalGoal,
    start_date: dateString,
    end_date: dateString,
    planned_capacity: z
      .coerce.number({ invalid_type_error: "Enter a number" })
      .int("Must be a whole number")
      .min(0, "Cannot be negative")
      .max(10000, "Value is too large"),
  })
  .superRefine((values, ctx) => {
    if (values.end_date < values.start_date) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "End date cannot be before start date",
        path: ["end_date"],
      });
    }
  });

export type EditSprintFormValues = z.infer<typeof editSprintSchema>;

export const completeSprintSchema = z.object({
  completed_points: z
    .coerce.number({ invalid_type_error: "Enter a number" })
    .int("Must be a whole number")
    .min(0, "Cannot be negative")
    .max(100000, "Value is too large"),
});

export type CompleteSprintFormValues = z.infer<typeof completeSprintSchema>;
```

### frontend/src/features/sprints/useSprintProjects.ts

```ts
import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { sprintsApi } from "./sprintsApi";
import type { SprintProjectOption } from "./types";

interface UseSprintProjectsResult {
  readonly projects: SprintProjectOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useSprintProjects(): UseSprintProjectsResult {
  const [projects, setProjects] = useState<SprintProjectOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await sprintsApi.listProjects();
        if (!cancelled) setProjects(result.items);
      } catch (err) {
        if (!cancelled) setError(toApiError(err));
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return { projects, isLoading, error };
}
```

### frontend/src/features/sprints/useSprints.ts

```ts
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { sprintsApi } from "./sprintsApi";
import type {
  CompleteSprintInput,
  CreateSprintInput,
  PaginatedSprints,
  Sprint,
  UpdateSprintInput,
} from "./types";

interface UseSprintsOptions {
  readonly limit: number;
}

interface UseSprintsResult {
  readonly data: PaginatedSprints | null;
  readonly filtered: Sprint[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly search: string;
  readonly projectId: string | null;
  readonly setSearch: (value: string) => void;
  readonly setProjectId: (value: string | null) => void;
  readonly setPage: (page: number) => void;
  readonly refresh: () => Promise<void>;
  readonly createSprint: (input: CreateSprintInput) => Promise<Sprint>;
  readonly updateSprint: (
    id: string,
    input: UpdateSprintInput,
  ) => Promise<Sprint>;
  readonly deleteSprint: (id: string) => Promise<void>;
  readonly startSprint: (id: string) => Promise<Sprint>;
  readonly completeSprint: (
    id: string,
    input: CompleteSprintInput,
  ) => Promise<Sprint>;
}

export function useSprints(
  options: UseSprintsOptions = { limit: 20 },
): UseSprintsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedSprints | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [search, setSearch] = useState<string>("");
  const [projectId, setProjectIdState] = useState<string | null>(null);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, projId: string | null) => {
      if (!projId) {
        setData(null);
        setIsLoading(false);
        return;
      }
      setIsLoading(true);
      setError(null);
      try {
        const result = await sprintsApi.list({
          project_id: projId,
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
        });
        if (!mounted.current) return;
        setData(result);
      } catch (err) {
        if (!mounted.current) return;
        setError(toApiError(err));
      } finally {
        if (mounted.current) setIsLoading(false);
      }
    },
    [limit],
  );

  useEffect(() => {
    mounted.current = true;
    void load(page, projectId);
    return () => {
      mounted.current = false;
    };
  }, [load, page, projectId]);

  const setProjectId = useCallback((value: string | null) => {
    setProjectIdState(value);
    setPage(1);
  }, []);

  const refresh = useCallback(async () => {
    await load(page, projectId);
  }, [load, page, projectId]);

  const createSprint = useCallback(
    async (input: CreateSprintInput) => {
      setIsMutating(true);
      try {
        const created = await sprintsApi.create(input);
        setProjectIdState(input.project_id);
        setPage(1);
        await load(1, input.project_id);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load],
  );

  const updateSprint = useCallback(
    async (id: string, input: UpdateSprintInput) => {
      setIsMutating(true);
      try {
        const updated = await sprintsApi.update(id, input);
        await load(page, projectId);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, projectId],
  );

  const deleteSprint = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await sprintsApi.remove(id);
        const remaining = (data?.items.length ?? 1) - 1;
        const nextPage = remaining <= 0 && page > 1 ? page - 1 : page;
        if (nextPage !== page) {
          setPage(nextPage);
        } else {
          await load(nextPage, projectId);
        }
      } finally {
        setIsMutating(false);
      }
    },
    [data, load, page, projectId],
  );

  const startSprint = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        const started = await sprintsApi.start(id);
        await load(page, projectId);
        return started;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, projectId],
  );

  const completeSprint = useCallback(
    async (id: string, input: CompleteSprintInput) => {
      setIsMutating(true);
      try {
        const completed = await sprintsApi.complete(id, input);
        await load(page, projectId);
        return completed;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, projectId],
  );

  const filtered = useMemo(() => {
    if (!data) return [];
    const term = search.trim().toLowerCase();
    if (!term) return data.items;
    return data.items.filter((sprint) => {
      return (
        sprint.name.toLowerCase().includes(term) ||
        (sprint.goal ?? "").toLowerCase().includes(term) ||
        sprint.status.toLowerCase().includes(term)
      );
    });
  }, [data, search]);

  const totalPages = data ? Math.max(1, Math.ceil(data.total / limit)) : 1;

  return {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    search,
    projectId,
    setSearch,
    setProjectId,
    setPage,
    refresh,
    createSprint,
    updateSprint,
    deleteSprint,
    startSprint,
    completeSprint,
  };
}
```

### frontend/src/features/sprints/components/SprintStatusBadge.tsx

```tsx
import { cn } from "@/lib/utils";

import type { SprintStatus } from "../types";

interface SprintStatusBadgeProps {
  readonly status: SprintStatus;
}

const STYLES: Record<SprintStatus, string> = {
  planned:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  active:
    "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
  completed:
    "border border-violet-500/40 bg-violet-500/10 text-violet-700 dark:text-violet-300",
  cancelled: "border border-border bg-muted text-muted-foreground",
};

const LABELS: Record<SprintStatus, string> = {
  planned: "Planned",
  active: "Active",
  completed: "Completed",
  cancelled: "Cancelled",
};

export function SprintStatusBadge({ status }: SprintStatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        STYLES[status],
      )}
    >
      {LABELS[status]}
    </span>
  );
}
```

### frontend/src/features/sprints/components/SprintFilters.tsx

```tsx
import { Search } from "lucide-react";

import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

import type { SprintProjectOption } from "../types";

interface SprintFiltersProps {
  readonly projects: SprintProjectOption[];
  readonly isLoadingProjects: boolean;
  readonly projectId: string | null;
  readonly onProjectChange: (id: string | null) => void;
  readonly search: string;
  readonly onSearchChange: (value: string) => void;
}

export function SprintFilters({
  projects,
  isLoadingProjects,
  projectId,
  onProjectChange,
  search,
  onSearchChange,
}: SprintFiltersProps) {
  return (
    <div className="flex flex-col gap-4 rounded-lg border border-border bg-card p-4 md:flex-row md:items-end md:justify-between">
      <div className="flex flex-1 flex-col gap-2 md:max-w-xs">
        <Label htmlFor="sprint-project">Project</Label>
        <select
          id="sprint-project"
          value={projectId ?? ""}
          onChange={(event) =>
            onProjectChange(event.target.value ? event.target.value : null)
          }
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          disabled={isLoadingProjects}
        >
          <option value="">
            {isLoadingProjects ? "Loading projects…" : "Select a project"}
          </option>
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name} ({project.key})
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-1 flex-col gap-2 md:max-w-sm">
        <Label htmlFor="sprint-search">Search</Label>
        <div className="relative">
          <Search
            aria-hidden="true"
            className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
          />
          <Input
            id="sprint-search"
            type="search"
            placeholder="Name, goal, or status…"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            className="pl-9"
            disabled={!projectId}
          />
        </div>
      </div>
    </div>
  );
}
```

### frontend/src/features/sprints/components/Pagination.tsx

```tsx
import { ChevronLeft, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/Button";

interface PaginationProps {
  readonly page: number;
  readonly totalPages: number;
  readonly total: number;
  readonly onChange: (page: number) => void;
}

export function Pagination({
  page,
  totalPages,
  total,
  onChange,
}: PaginationProps) {
  const canPrev = page > 1;
  const canNext = page < totalPages;

  return (
    <div className="flex flex-col items-center justify-between gap-3 border-t border-border pt-4 text-sm text-muted-foreground sm:flex-row">
      <p>
        Page <span className="font-medium text-foreground">{page}</span> of{" "}
        <span className="font-medium text-foreground">{totalPages}</span>
        <span className="mx-2 opacity-50">•</span>
        <span>{total} total</span>
      </p>
      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => onChange(page - 1)}
          disabled={!canPrev}
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </Button>
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => onChange(page + 1)}
          disabled={!canNext}
        >
          Next
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
```

### frontend/src/features/sprints/components/Modal.tsx

```tsx
import { X } from "lucide-react";
import { useEffect } from "react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

interface ModalProps {
  readonly open: boolean;
  readonly title: string;
  readonly description?: string;
  readonly onClose: () => void;
  readonly children: React.ReactNode;
  readonly maxWidthClassName?: string;
}

export function Modal({
  open,
  title,
  description,
  onClose,
  children,
  maxWidthClassName = "max-w-lg",
}: ModalProps) {
  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={title}
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <div
        role="presentation"
        onClick={onClose}
        className="absolute inset-0 bg-background/70 backdrop-blur-sm"
      />
      <div
        className={cn(
          "relative w-full rounded-lg border border-border bg-card p-6 shadow-lg",
          maxWidthClassName,
        )}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold">{title}</h2>
            {description && (
              <p className="mt-1 text-sm text-muted-foreground">
                {description}
              </p>
            )}
          </div>
          <Button
            type="button"
            variant="ghost"
            size="icon"
            aria-label="Close dialog"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
}
```

### frontend/src/features/sprints/components/SprintsTable.tsx

```tsx
import { Flag, Pencil, PlayCircle, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type { Sprint } from "../types";
import { SprintStatusBadge } from "./SprintStatusBadge";

interface SprintsTableProps {
  readonly sprints: Sprint[];
  readonly onEdit: (sprint: Sprint) => void;
  readonly onDelete: (sprint: Sprint) => void;
  readonly onStart: (sprint: Sprint) => void;
  readonly onComplete: (sprint: Sprint) => void;
  readonly isMutating: boolean;
}

function formatDate(value: string | null): string {
  if (!value) return "—";
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) return value;
  return new Date(parsed).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });
}

function percent(sprint: Sprint): string {
  if (sprint.planned_capacity <= 0) return "—";
  const value = (sprint.completed_points / sprint.planned_capacity) * 100;
  return `${Math.min(999, Math.max(0, Math.round(value)))}%`;
}

export function SprintsTable({
  sprints,
  onEdit,
  onDelete,
  onStart,
  onComplete,
  isMutating,
}: SprintsTableProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Name
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Window
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Capacity
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Completion
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {sprints.map((sprint) => {
              const canStart = sprint.status === "planned";
              const canComplete = sprint.status === "active";
              const canEdit =
                sprint.status !== "completed" && sprint.status !== "cancelled";
              const canDelete = sprint.status !== "completed";

              return (
                <tr
                  key={sprint.id}
                  className={cn(
                    "transition-colors hover:bg-muted/30",
                    sprint.status === "cancelled" && "opacity-70",
                  )}
                >
                  <td className="px-4 py-3">
                    <div className="flex flex-col">
                      <span className="font-medium text-foreground">
                        {sprint.name}
                      </span>
                      {sprint.goal && (
                        <span className="line-clamp-1 text-xs text-muted-foreground">
                          {sprint.goal}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <SprintStatusBadge status={sprint.status} />
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    <div className="flex flex-col">
                      <span>{formatDate(sprint.start_date)}</span>
                      <span className="text-xs opacity-80">
                        → {formatDate(sprint.end_date)}
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    {sprint.planned_capacity}
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    <div className="flex flex-col">
                      <span>
                        {sprint.completed_points} / {sprint.planned_capacity}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {percent(sprint)}
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-1">
                      {canStart && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          aria-label={`Start ${sprint.name}`}
                          onClick={() => onStart(sprint)}
                          disabled={isMutating}
                          title="Start sprint"
                        >
                          <PlayCircle className="h-4 w-4" />
                        </Button>
                      )}
                      {canComplete && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          aria-label={`Complete ${sprint.name}`}
                          onClick={() => onComplete(sprint)}
                          disabled={isMutating}
                          title="Complete sprint"
                        >
                          <Flag className="h-4 w-4" />
                        </Button>
                      )}
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Edit ${sprint.name}`}
                        onClick={() => onEdit(sprint)}
                        disabled={isMutating || !canEdit}
                        title="Edit sprint"
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Delete ${sprint.name}`}
                        onClick={() => onDelete(sprint)}
                        disabled={isMutating || !canDelete}
                        title={
                          canDelete
                            ? "Delete sprint"
                            : "Completed sprints cannot be deleted"
                        }
                        className="text-destructive hover:bg-destructive/10 hover:text-destructive disabled:text-muted-foreground"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

### frontend/src/features/sprints/components/CreateSprintDialog.tsx

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import {
  createSprintSchema,
  type CreateSprintFormValues,
} from "../sprintSchemas";
import type { CreateSprintInput, SprintProjectOption } from "../types";
import { Modal } from "./Modal";

interface CreateSprintDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateSprintInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly projects: SprintProjectOption[];
  readonly projectsLoading: boolean;
  readonly defaultProjectId: string | null;
}

export function CreateSprintDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
  projects,
  projectsLoading,
  defaultProjectId,
}: CreateSprintDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateSprintFormValues>({
    resolver: zodResolver(createSprintSchema),
    defaultValues: {
      project_id: defaultProjectId ?? "",
      name: "",
      goal: "",
      start_date: "",
      end_date: "",
      planned_capacity: 0,
    },
  });

  useEffect(() => {
    if (open) {
      reset({
        project_id: defaultProjectId ?? "",
        name: "",
        goal: "",
        start_date: "",
        end_date: "",
        planned_capacity: 0,
      });
    }
  }, [open, defaultProjectId, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: CreateSprintInput = {
        project_id: values.project_id,
        name: values.name.trim(),
        goal: values.goal ? values.goal.trim() : null,
        start_date: values.start_date,
        end_date: values.end_date,
        planned_capacity: values.planned_capacity,
      };
      await onSubmit(input);
      toast({ title: "Sprint created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create sprint"
      description="Time-box a scope of work and track its outcome."
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="create-project">Project</Label>
          <select
            id="create-project"
            {...register("project_id")}
            disabled={projectsLoading}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            aria-invalid={Boolean(errors.project_id)}
          >
            <option value="">
              {projectsLoading ? "Loading projects…" : "Select a project"}
            </option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name} ({project.key})
              </option>
            ))}
          </select>
          {errors.project_id && (
            <p className="text-xs text-destructive">
              {errors.project_id.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="create-name">Name</Label>
          <Input
            id="create-name"
            placeholder="e.g. Sprint 12 — Onboarding polish"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="create-goal">Goal</Label>
          <textarea
            id="create-goal"
            rows={3}
            {...register("goal")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="What outcome should this sprint deliver?"
          />
          {errors.goal && (
            <p className="text-xs text-destructive">{errors.goal.message}</p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="create-start">Start date</Label>
            <Input
              id="create-start"
              type="date"
              {...register("start_date")}
              aria-invalid={Boolean(errors.start_date)}
            />
            {errors.start_date && (
              <p className="text-xs text-destructive">
                {errors.start_date.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="create-end">End date</Label>
            <Input
              id="create-end"
              type="date"
              {...register("end_date")}
              aria-invalid={Boolean(errors.end_date)}
            />
            {errors.end_date && (
              <p className="text-xs text-destructive">
                {errors.end_date.message}
              </p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="create-capacity">Planned capacity (points)</Label>
          <Input
            id="create-capacity"
            type="number"
            min={0}
            step={1}
            {...register("planned_capacity")}
            aria-invalid={Boolean(errors.planned_capacity)}
          />
          {errors.planned_capacity && (
            <p className="text-xs text-destructive">
              {errors.planned_capacity.message}
            </p>
          )}
        </div>

        <div className="flex items-center justify-end gap-2 pt-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={submitting}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating…
              </>
            ) : (
              "Create sprint"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
```

### frontend/src/features/sprints/components/EditSprintDialog.tsx

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import {
  editSprintSchema,
  type EditSprintFormValues,
} from "../sprintSchemas";
import type { Sprint, UpdateSprintInput } from "../types";
import { Modal } from "./Modal";

interface EditSprintDialogProps {
  readonly open: boolean;
  readonly sprint: Sprint | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateSprintInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function EditSprintDialog({
  open,
  sprint,
  onClose,
  onSubmit,
  isSubmitting,
}: EditSprintDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditSprintFormValues>({
    resolver: zodResolver(editSprintSchema),
    defaultValues: {
      name: "",
      goal: "",
      start_date: "",
      end_date: "",
      planned_capacity: 0,
    },
  });

  useEffect(() => {
    if (open && sprint) {
      reset({
        name: sprint.name,
        goal: sprint.goal ?? "",
        start_date: sprint.start_date,
        end_date: sprint.end_date,
        planned_capacity: sprint.planned_capacity,
      });
    }
  }, [open, sprint, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!sprint) return;
    try {
      const input: UpdateSprintInput = {
        name: values.name.trim(),
        goal: values.goal ? values.goal.trim() : null,
        start_date: values.start_date,
        end_date: values.end_date,
        planned_capacity: values.planned_capacity,
      };
      await onSubmit(sprint.id, input);
      toast({ title: "Sprint updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && sprint !== null}
      onClose={onClose}
      title={`Edit ${sprint?.name ?? "sprint"}`}
      description={sprint ? `Status: ${sprint.status}` : undefined}
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="edit-name">Name</Label>
          <Input
            id="edit-name"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="edit-goal">Goal</Label>
          <textarea
            id="edit-goal"
            rows={3}
            {...register("goal")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          {errors.goal && (
            <p className="text-xs text-destructive">{errors.goal.message}</p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="edit-start">Start date</Label>
            <Input
              id="edit-start"
              type="date"
              {...register("start_date")}
              aria-invalid={Boolean(errors.start_date)}
            />
            {errors.start_date && (
              <p className="text-xs text-destructive">
                {errors.start_date.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-end">End date</Label>
            <Input
              id="edit-end"
              type="date"
              {...register("end_date")}
              aria-invalid={Boolean(errors.end_date)}
            />
            {errors.end_date && (
              <p className="text-xs text-destructive">
                {errors.end_date.message}
              </p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="edit-capacity">Planned capacity (points)</Label>
          <Input
            id="edit-capacity"
            type="number"
            min={0}
            step={1}
            {...register("planned_capacity")}
            aria-invalid={Boolean(errors.planned_capacity)}
          />
          {errors.planned_capacity && (
            <p className="text-xs text-destructive">
              {errors.planned_capacity.message}
            </p>
          )}
        </div>

        <div className="flex items-center justify-end gap-2 pt-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={submitting || !isDirty}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Saving…
              </>
            ) : (
              "Save changes"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
```

### frontend/src/features/sprints/components/CompleteSprintDialog.tsx

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import {
  completeSprintSchema,
  type CompleteSprintFormValues,
} from "../sprintSchemas";
import type { CompleteSprintInput, Sprint } from "../types";
import { Modal } from "./Modal";

interface CompleteSprintDialogProps {
  readonly open: boolean;
  readonly sprint: Sprint | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: CompleteSprintInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function CompleteSprintDialog({
  open,
  sprint,
  onClose,
  onSubmit,
  isSubmitting,
}: CompleteSprintDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CompleteSprintFormValues>({
    resolver: zodResolver(completeSprintSchema),
    defaultValues: { completed_points: 0 },
  });

  useEffect(() => {
    if (open && sprint) {
      reset({ completed_points: sprint.planned_capacity });
    }
  }, [open, sprint, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!sprint) return;
    try {
      await onSubmit(sprint.id, {
        completed_points: values.completed_points,
      });
      toast({ title: "Sprint completed", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not complete sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && sprint !== null}
      onClose={onClose}
      title={`Complete ${sprint?.name ?? "sprint"}`}
      description="Record the final velocity for this sprint."
      maxWidthClassName="max-w-md"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="completed-points">Completed points</Label>
          <Input
            id="completed-points"
            type="number"
            min={0}
            step={1}
            {...register("completed_points")}
            aria-invalid={Boolean(errors.completed_points)}
          />
          {sprint && (
            <p className="text-xs text-muted-foreground">
              Planned capacity: {sprint.planned_capacity}
            </p>
          )}
          {errors.completed_points && (
            <p className="text-xs text-destructive">
              {errors.completed_points.message}
            </p>
          )}
        </div>

        <div className="flex items-center justify-end gap-2 pt-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={submitting}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Completing…
              </>
            ) : (
              "Complete sprint"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
```

### frontend/src/features/sprints/components/DeleteSprintDialog.tsx

```tsx
import { Loader2, TriangleAlert } from "lucide-react";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { useToast } from "@/providers/ToastProvider";

import type { Sprint } from "../types";
import { Modal } from "./Modal";

interface DeleteSprintDialogProps {
  readonly open: boolean;
  readonly sprint: Sprint | null;
  readonly onClose: () => void;
  readonly onConfirm: (id: string) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function DeleteSprintDialog({
  open,
  sprint,
  onClose,
  onConfirm,
  isSubmitting,
}: DeleteSprintDialogProps) {
  const { toast } = useToast();

  const handleConfirm = async () => {
    if (!sprint) return;
    try {
      await onConfirm(sprint.id);
      toast({ title: "Sprint deleted", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not delete sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  };

  return (
    <Modal
      open={open && sprint !== null}
      onClose={onClose}
      title="Delete sprint"
      maxWidthClassName="max-w-md"
    >
      <div className="space-y-4">
        <div className="flex items-start gap-3 rounded-md border border-destructive/40 bg-destructive/10 p-3 text-destructive">
          <TriangleAlert className="mt-0.5 h-5 w-5" aria-hidden="true" />
          <div className="text-sm">
            <p className="font-medium">This action cannot be undone.</p>
            <p className="mt-1 opacity-90">
              {sprint ? (
                <>
                  You are about to permanently remove{" "}
                  <span className="font-semibold">{sprint.name}</span>.
                </>
              ) : (
                "Sprint details are unavailable."
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-end gap-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="destructive"
            onClick={() => void handleConfirm()}
            disabled={isSubmitting || !sprint}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Deleting…
              </>
            ) : (
              "Delete sprint"
            )}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
```

### frontend/src/features/sprints/components/SprintsErrorState.tsx

```tsx
import { AlertCircle } from "lucide-react";

import { Button } from "@/components/ui/Button";

interface SprintsErrorStateProps {
  readonly message: string;
  readonly onRetry: () => void;
}

export function SprintsErrorState({
  message,
  onRetry,
}: SprintsErrorStateProps) {
  return (
    <div
      role="alert"
      className="flex flex-col items-center justify-center gap-3 rounded-lg border border-destructive/40 bg-destructive/10 p-8 text-center text-destructive"
    >
      <AlertCircle className="h-6 w-6" aria-hidden="true" />
      <div>
        <h3 className="text-base font-semibold">Failed to load sprints</h3>
        <p className="mt-1 text-sm opacity-90">{message}</p>
      </div>
      <Button
        type="button"
        variant="outline"
        onClick={onRetry}
        className="border-destructive/40 text-destructive hover:bg-destructive/20"
      >
        Try again
      </Button>
    </div>
  );
}
```

### frontend/src/features/sprints/components/SprintsLoadingState.tsx

```tsx
export function SprintsLoadingState() {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="divide-y divide-border">
        {Array.from({ length: 5 }).map((_, index) => (
          <div key={index} className="flex items-center gap-4 p-4">
            <div className="h-4 flex-1 animate-pulse rounded bg-muted" />
            <div className="h-4 w-20 animate-pulse rounded bg-muted" />
            <div className="h-4 w-32 animate-pulse rounded bg-muted" />
            <div className="h-4 w-16 animate-pulse rounded bg-muted" />
            <div className="h-8 w-24 animate-pulse rounded bg-muted" />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### frontend/src/features/sprints/index.ts

```ts
export { sprintsApi } from "./sprintsApi";
export { useSprints } from "./useSprints";
export { useSprintProjects } from "./useSprintProjects";
export type {
  CompleteSprintInput,
  CreateSprintInput,
  PaginatedSprintProjects,
  PaginatedSprints,
  Sprint,
  SprintListParams,
  SprintProjectOption,
  SprintStatus,
  UpdateSprintInput,
} from "./types";
export { CompleteSprintDialog } from "./components/CompleteSprintDialog";
export { CreateSprintDialog } from "./components/CreateSprintDialog";
export { DeleteSprintDialog } from "./components/DeleteSprintDialog";
export { EditSprintDialog } from "./components/EditSprintDialog";
export { Pagination } from "./components/Pagination";
export { SprintFilters } from "./components/SprintFilters";
export { SprintStatusBadge } from "./components/SprintStatusBadge";
export { SprintsErrorState } from "./components/SprintsErrorState";
export { SprintsLoadingState } from "./components/SprintsLoadingState";
export { SprintsTable } from "./components/SprintsTable";
```

### frontend/src/pages/sprints/SprintsPage.tsx

```tsx
import { Plus } from "lucide-react";
import { useState } from "react";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CompleteSprintDialog,
  CreateSprintDialog,
  DeleteSprintDialog,
  EditSprintDialog,
  Pagination,
  SprintFilters,
  SprintsErrorState,
  SprintsLoadingState,
  SprintsTable,
  useSprintProjects,
  useSprints,
  type Sprint,
} from "@/features/sprints";
import { useToast } from "@/providers/ToastProvider";

const PAGE_SIZE = 20;

export default function SprintsPage() {
  const {
    projects,
    isLoading: projectsLoading,
    error: projectsError,
  } = useSprintProjects();

  const {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    search,
    projectId,
    setSearch,
    setProjectId,
    setPage,
    refresh,
    createSprint,
    updateSprint,
    deleteSprint,
    startSprint,
    completeSprint,
  } = useSprints({ limit: PAGE_SIZE });

  const { toast } = useToast();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<Sprint | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Sprint | null>(null);
  const [completeTarget, setCompleteTarget] = useState<Sprint | null>(null);

  const handleStart = async (sprint: Sprint) => {
    try {
      await startSprint(sprint.id);
      toast({ title: `${sprint.name} started`, variant: "success" });
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not start sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  };

  const hasProjects = projects.length > 0;
  const hasResults = filtered.length > 0;
  const totalCount = data?.total ?? 0;
  const canCreate = hasProjects;

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Sprints</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Plan, run, and close sprints tied to your projects.
          </p>
        </div>
        <Button
          type="button"
          onClick={() => setCreateOpen(true)}
          disabled={!canCreate || projectsLoading}
        >
          <Plus className="h-4 w-4" />
          New sprint
        </Button>
      </header>

      <SprintFilters
        projects={projects}
        isLoadingProjects={projectsLoading}
        projectId={projectId}
        onProjectChange={setProjectId}
        search={search}
        onSearchChange={setSearch}
      />

      {projectsError ? (
        <SprintsErrorState
          message={projectsError.message}
          onRetry={() => window.location.reload()}
        />
      ) : !projectsLoading && !hasProjects ? (
        <EmptyState
          title="No projects available"
          description="Create a project first to start planning sprints."
        />
      ) : !projectId ? (
        <EmptyState
          title="Select a project"
          description="Pick a project above to view or create its sprints."
        />
      ) : isLoading && !data ? (
        <SprintsLoadingState />
      ) : error ? (
        <SprintsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            search
              ? "No sprints match your search"
              : "No sprints in this project yet"
          }
          description={
            search
              ? "Try a different name, goal, or status — or clear the search."
              : "Create the first sprint to start tracking delivery."
          }
          action={
            search ? (
              <Button
                type="button"
                variant="outline"
                onClick={() => setSearch("")}
              >
                Clear search
              </Button>
            ) : (
              <Button type="button" onClick={() => setCreateOpen(true)}>
                <Plus className="h-4 w-4" />
                New sprint
              </Button>
            )
          }
        />
      ) : (
        <div className="space-y-4">
          <SprintsTable
            sprints={filtered}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
            onStart={(sprint) => void handleStart(sprint)}
            onComplete={setCompleteTarget}
          />
          <Pagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateSprintDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createSprint(input);
        }}
        isSubmitting={isMutating}
        projects={projects}
        projectsLoading={projectsLoading}
        defaultProjectId={projectId}
      />

      <EditSprintDialog
        open={editTarget !== null}
        sprint={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateSprint(id, input);
        }}
        isSubmitting={isMutating}
      />

      <CompleteSprintDialog
        open={completeTarget !== null}
        sprint={completeTarget}
        onClose={() => setCompleteTarget(null)}
        onSubmit={async (id, input) => {
          await completeSprint(id, input);
        }}
        isSubmitting={isMutating}
      />

      <DeleteSprintDialog
        open={deleteTarget !== null}
        sprint={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteSprint(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
```

---

### MANUAL ROUTER PATCH

Wire the new `SprintsPage` into `src/router/AppRouter.tsx` without altering any other lines.

1. Add this lazy import next to the other page imports at the top of `src/router/AppRouter.tsx`:

```tsx
const SprintsPage = lazy(() => import("@/pages/sprints/SprintsPage"));
```

2. Inside the protected `<Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>` block, replace:

```tsx
<Route
  path={ROUTES.SPRINTS}
  element={<ModulePlaceholder title="Sprints" />}
/>
```

with:

```tsx
<Route path={ROUTES.SPRINTS} element={<SprintsPage />} />
```

No other lines in `AppRouter.tsx` need to change.