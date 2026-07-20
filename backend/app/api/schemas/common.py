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