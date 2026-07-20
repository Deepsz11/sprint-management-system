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