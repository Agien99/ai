from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


RouletteNumber = Annotated[
    int,
    Field(
        ge=0,
        le=36,
    ),
]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class SessionResponse(BaseModel):
    session_id: UUID
    status: str
    initial_spin_count: int
    started_at: datetime
    ended_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class InitialSpinsRequest(BaseModel):
    spins: list[RouletteNumber] = Field(
        min_length=10,
        max_length=15,
    )