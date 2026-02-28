from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from app.core.enums import GenderEnum, GenerationSourceEnum, SlotEnum, TpoEnum


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ItemBase(BaseModel):
    category: str
    sub_category: str
    gender: GenderEnum
    fit: str
    color_tone: str
    moods: list[str] = Field(default_factory=list)
    tpos: list[TpoEnum] = Field(default_factory=list)
    temperature_min: int
    temperature_max: int
    price_krw: int
    stock_qty: int = 0
    image_url: str
    location_zone: str | None = None
    is_active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    category: str | None = None
    sub_category: str | None = None
    gender: GenderEnum | None = None
    fit: str | None = None
    color_tone: str | None = None
    moods: list[str] | None = None
    tpos: list[TpoEnum] | None = None
    temperature_min: int | None = None
    temperature_max: int | None = None
    price_krw: int | None = None
    stock_qty: int | None = None
    image_url: str | None = None
    location_zone: str | None = None
    is_active: bool | None = None


class ItemRecord(ItemBase):
    item_id: str
    created_at: str
    updated_at: str


class OutfitItemLink(BaseModel):
    item_id: str
    slot: SlotEnum
    sort_order: int = 0


class OutfitBase(BaseModel):
    title: str
    subtitle: str | None = None
    gender_target: GenderEnum
    tpo: TpoEnum
    mood: str | None = None
    total_price_krw: int
    generation_source: GenerationSourceEnum
    score: float | None = None
    created_by: str | None = None
    items: list[OutfitItemLink] = Field(default_factory=list)


class OutfitCreate(OutfitBase):
    pass


class OutfitUpdate(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    gender_target: GenderEnum | None = None
    tpo: TpoEnum | None = None
    mood: str | None = None
    total_price_krw: int | None = None
    generation_source: GenerationSourceEnum | None = None
    score: float | None = None
    created_by: str | None = None
    items: list[OutfitItemLink] | None = None


class OutfitRecord(OutfitBase):
    outfit_id: str
    created_at: str


class StoreSettingsRecord(BaseModel):
    store_id: str = "default"
    target_gender: GenderEnum = GenderEnum.UNISEX
    price_band_min_krw: int | None = None
    price_band_max_krw: int | None = None
    mood_weights: dict[str, float] = Field(default_factory=dict)
    updated_at: str = Field(default_factory=utc_now_iso)


class StoreSettingsUpdate(BaseModel):
    target_gender: GenderEnum | None = None
    price_band_min_krw: int | None = None
    price_band_max_krw: int | None = None
    mood_weights: dict[str, float] | None = None


class DashboardSummary(BaseModel):
    items_total: int
    outfits_total: int
    low_stock_count: int


class DashboardTop3(BaseModel):
    outfits: list[dict[str, Any]]


class DashboardTpoRatio(BaseModel):
    tpo_ratio: dict[str, float]


class DashboardLowStock(BaseModel):
    items: list[dict[str, Any]]
