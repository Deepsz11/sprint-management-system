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