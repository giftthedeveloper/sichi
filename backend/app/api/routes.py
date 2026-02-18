from __future__ import annotations

from fastapi import APIRouter, Query

from app import service
from app.models import Profile
from app.schemas import HealthResponse, ProfileCreateRequest, ProfileResponse

router = APIRouter(prefix="/api")


def _profile_to_schema(profile: Profile) -> ProfileResponse:
    return ProfileResponse(id=profile.id, name=profile.name)


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/profiles", response_model=list[ProfileResponse])
def list_profiles(query: str = Query(default="")) -> list[ProfileResponse]:
    profiles = service.list_profiles(query=query)
    return [_profile_to_schema(profile) for profile in profiles]


@router.post("/profiles", response_model=ProfileResponse)
def create_profile(payload: ProfileCreateRequest) -> ProfileResponse:
    profile = service.create_profile(payload.name)
    return _profile_to_schema(profile)
