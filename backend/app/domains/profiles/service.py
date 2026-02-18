from __future__ import annotations

from app.domains.profiles.models import Profile
from app.domains.profiles import repository


def list_profiles(query: str | None) -> list[Profile]:
    if not query:
        return []
    needle = query.strip()
    if not needle:
        return []
    return repository.list_by_query(needle)


def create_profile(name: str) -> Profile:
    return repository.create(name)
