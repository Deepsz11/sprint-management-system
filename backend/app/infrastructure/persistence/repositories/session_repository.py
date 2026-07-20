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