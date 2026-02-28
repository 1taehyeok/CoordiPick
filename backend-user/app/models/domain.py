from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Item:
    item_id: str
    name: str
    slot: str
    gender: str
    tpos: list[str]
    moods: list[str]
    temperature_min: float
    temperature_max: float
    price_krw: int
    image_url: str
    location_zone: str = ""
    is_active: bool = True


@dataclass(slots=True)
class ScoredItem:
    item: Item
    score: float
    reason_tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ComposedRecommendation:
    recommendation_id: str
    title: str
    subtitle: str
    total_price_krw: int
    thumbnail_url: str
    reason_tags: list[str]
    items: list[Item]
    score: float
    created_at: datetime


@dataclass(slots=True)
class Event:
    event_id: str
    session_id: str
    event_type: str
    recommendation_id: str
    payload: dict
    created_at: datetime
