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