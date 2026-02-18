from __future__ import annotations

from app.models import Profile
from app.store import store


def list_profiles(query: str | None) -> list[Profile]:
    if not query:
        return []
    needle = query.strip().lower()
    if not needle:
        return []
    return [profile for profile in store.profiles.values() if needle in profile.name.lower()]


def create_profile(name: str) -> Profile:
    profile = Profile(id=f"u-{len(store.profiles) + 1}", name=name.strip())
    store.profiles[profile.id] = profile
    return profile
