from __future__ import annotations

from dataclasses import dataclass, field

from app.models import Profile


@dataclass(slots=True)
class InMemoryStore:
    profiles: dict[str, Profile] = field(default_factory=dict)


store = InMemoryStore(
    profiles={
        "u-1": Profile(id="u-1", name="Amaka Eze"),
        "u-2": Profile(id="u-2", name="Tosin Akin"),
        "u-3": Profile(id="u-3", name="Sade Bello"),
    }
)
