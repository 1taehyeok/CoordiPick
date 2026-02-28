from dataclasses import dataclass, field

from app.models.admin import (
    ItemCreate,
    ItemRecord,
    OutfitCreate,
    OutfitRecord,
    StoreSettingsRecord,
    utc_now_iso,
)


@dataclass
class InMemoryAdminRepository:
    items: dict[str, ItemRecord] = field(default_factory=dict)
    outfits: dict[str, OutfitRecord] = field(default_factory=dict)
    store_settings: StoreSettingsRecord = field(default_factory=StoreSettingsRecord)
    next_item_id: int = 1
    next_outfit_id: int = 1

    def list_items(self) -> list[ItemRecord]:
        return list(self.items.values())

    def create_item(self, payload: ItemCreate) -> ItemRecord:
        item_id = str(self.next_item_id)
        self.next_item_id += 1
        now = utc_now_iso()
        item = ItemRecord(item_id=item_id, created_at=now, updated_at=now, **payload.model_dump())
        self.items[item_id] = item
        return item

    def get_item(self, item_id: str) -> ItemRecord | None:
        return self.items.get(item_id)

    def update_item(self, item_id: str, update_data: dict) -> ItemRecord | None:
        item = self.items.get(item_id)
        if item is None:
            return None
        updated = item.model_copy(update={**update_data, "updated_at": utc_now_iso()})
        self.items[item_id] = updated
        return updated

    def delete_item(self, item_id: str) -> bool:
        return self.items.pop(item_id, None) is not None

    def list_outfits(self) -> list[OutfitRecord]:
        return list(self.outfits.values())

    def create_outfit(self, payload: OutfitCreate) -> OutfitRecord:
        outfit_id = str(self.next_outfit_id)
        self.next_outfit_id += 1
        outfit = OutfitRecord(outfit_id=outfit_id, created_at=utc_now_iso(), **payload.model_dump())
        self.outfits[outfit_id] = outfit
        return outfit

    def get_outfit(self, outfit_id: str) -> OutfitRecord | None:
        return self.outfits.get(outfit_id)

    def update_outfit(self, outfit_id: str, update_data: dict) -> OutfitRecord | None:
        outfit = self.outfits.get(outfit_id)
        if outfit is None:
            return None
        updated = outfit.model_copy(update=update_data)
        self.outfits[outfit_id] = updated
        return updated

    def delete_outfit(self, outfit_id: str) -> bool:
        return self.outfits.pop(outfit_id, None) is not None

    def get_store_settings(self) -> StoreSettingsRecord:
        return self.store_settings

    def update_store_settings(self, update_data: dict) -> StoreSettingsRecord:
        self.store_settings = self.store_settings.model_copy(
            update={**update_data, "updated_at": utc_now_iso()}
        )
        return self.store_settings

    def reset(self) -> None:
        self.items.clear()
        self.outfits.clear()
        self.store_settings = StoreSettingsRecord()
        self.next_item_id = 1
        self.next_outfit_id = 1
