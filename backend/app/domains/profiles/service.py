from __future__ import annotations

from typing import Optional

from app.domains.profiles.models import Profile
from app.domains.profiles import repository


def list_profiles(query: Optional[str]) -> list[Profile]:
    if not query:
        return []
    needle = query.strip()
    if not needle:
        return []
    return repository.list_by_query(needle)


def create_profile(name: str) -> Profile:
    return repository.create(name)


def get_profile(profile_id: str) -> Optional[Profile]:
    return repository.get_by_id(profile_id)
