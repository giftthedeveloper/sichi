from __future__ import annotations

from fastapi import APIRouter, Query

from app.domains.profiles.models import Profile
from app.domains.profiles.schemas import ProfileCreateRequest, ProfileResponse
from app.domains.profiles import service

router = APIRouter(prefix="/profiles", tags=["profiles"])


def to_schema(profile: Profile) -> ProfileResponse:
    return ProfileResponse(id=profile.id, name=profile.name)


@router.get("", response_model=list[ProfileResponse])
def list_profiles(query: str = Query(default="")) -> list[ProfileResponse]:
    profiles = service.list_profiles(query=query)
    return [to_schema(profile) for profile in profiles]


@router.post("", response_model=ProfileResponse)
def create_profile(payload: ProfileCreateRequest) -> ProfileResponse:
    profile = service.create_profile(payload.name)
    return to_schema(profile)
