from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Gender(str, Enum):
    male = "male"
    female = "female"
    unisex = "unisex"


class TPO(str, Enum):
    commute = "commute"
    date = "date"
    friends = "friends"
    travel = "travel"
    daily = "daily"
    special = "special"


class Slot(str, Enum):
    top = "top"
    bottom = "bottom"
    outer = "outer"
    shoes = "shoes"
    acc = "acc"


class EventType(str, Enum):
    impression = "impression"
    click = "click"
    detail_view = "detail_view"


class GenerateRecommendationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str
    gender: Gender
    tpo: TPO
    mood: str | None = None
    temperature_c: float


class RecommendationCard(BaseModel):
    model_config = ConfigDict(extra="forbid")
    recommendation_id: str
    title: str
    subtitle: str | None = None
    total_price_krw: int
    thumbnail_url: str
    reason_tags: list[str] | None = None


class RecommendationListData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    cards: list[RecommendationCard] = Field(min_length=1, max_length=6)


class RecommendationListMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    generated_at: datetime | None = None


class RecommendationListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool = True
    data: RecommendationListData
    meta: RecommendationListMeta | None = None


class OutfitItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item_id: str
    name: str
    slot: Slot
    price_krw: int
    location_zone: str | None = None
    image_url: str


class RecommendationDetailData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    recommendation_id: str
    title: str
    subtitle: str | None = None
    total_price_krw: int
    items: list[OutfitItem]


class RecommendationDetailResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool = True
    data: RecommendationDetailData


class CreateEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str
    event_type: EventType
    recommendation_id: str
    payload: dict[str, Any] | None = None


class EnvelopeSimpleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool
    data: dict[str, Any]


class ErrorPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str
    message: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool = False
    error: ErrorPayload
