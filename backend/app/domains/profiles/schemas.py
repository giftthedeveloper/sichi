from __future__ import annotations

from pydantic import BaseModel, Field


class ProfileCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class ProfileResponse(BaseModel):
    id: str
    name: str
