from collections import Counter

from app.core.errors import ApiError
from app.models.admin import (
    DashboardLowStock,
    DashboardSummary,
    DashboardTop3,
    DashboardTpoRatio,
    ItemCreate,
    ItemUpdate,
    OutfitItemLink,
    OutfitCreate,
    OutfitUpdate,
    StoreSettingsUpdate,
)
from app.repositories.memory import InMemoryAdminRepository


class AdminService:
    def __init__(self, repo: InMemoryAdminRepository) -> None:
        self.repo = repo

    def list_items(self) -> list[dict]:
        return [item.model_dump() for item in self.repo.list_items()]

    def create_item(self, payload: ItemCreate) -> dict:
        return self.repo.create_item(payload).model_dump()

    def update_item(self, item_id: str, payload: ItemUpdate) -> dict:
        update_data = payload.model_dump(exclude_unset=True)
        item = self.repo.update_item(item_id, update_data)
        if item is None:
            raise ApiError(code="NOT_FOUND", message="item not found", status_code=404)
        return item.model_dump()

    def delete_item(self, item_id: str) -> None:
        if not self.repo.delete_item(item_id):
            raise ApiError(code="NOT_FOUND", message="item not found", status_code=404)

    def list_outfits(self) -> list[dict]:
        return [outfit.model_dump() for outfit in self.repo.list_outfits()]

    def create_outfit(self, payload: OutfitCreate) -> dict:
        for item_link in payload.items:
            if self.repo.get_item(item_link.item_id) is None:
                raise ApiError(
                    code="INVALID_INPUT",
                    message="outfit references missing item",
                    status_code=400,
                    details={"item_id": item_link.item_id},
                )
        return self.repo.create_outfit(payload).model_dump()

    def update_outfit(self, outfit_id: str, payload: OutfitUpdate) -> dict:
        update_data = payload.model_dump(exclude_unset=True)
        if "items" in update_data:
            normalized_items: list[OutfitItemLink] = []
            for item_link in update_data["items"]:
                normalized = OutfitItemLink.model_validate(item_link)
                item_id = normalized.item_id
                if self.repo.get_item(item_id) is None:
                    raise ApiError(
                        code="INVALID_INPUT",
                        message="outfit references missing item",
                        status_code=400,
                        details={"item_id": item_id},
                    )
                normalized_items.append(normalized)
            update_data["items"] = normalized_items

        outfit = self.repo.update_outfit(outfit_id, update_data)
        if outfit is None:
            raise ApiError(code="NOT_FOUND", message="outfit not found", status_code=404)
        return outfit.model_dump()

    def delete_outfit(self, outfit_id: str) -> None:
        if not self.repo.delete_outfit(outfit_id):
            raise ApiError(code="NOT_FOUND", message="outfit not found", status_code=404)

    def get_store_settings(self) -> dict:
        return self.repo.get_store_settings().model_dump()

    def update_store_settings(self, payload: StoreSettingsUpdate) -> dict:
        update_data = payload.model_dump(exclude_unset=True)
        if (
            "price_band_min_krw" in update_data
            and "price_band_max_krw" in update_data
            and update_data["price_band_min_krw"] is not None
            and update_data["price_band_max_krw"] is not None
            and update_data["price_band_min_krw"] > update_data["price_band_max_krw"]
        ):
            raise ApiError(
                code="INVALID_INPUT",
                message="price_band_min_krw must be <= price_band_max_krw",
                status_code=400,
            )
        return self.repo.update_store_settings(update_data).model_dump()

    def get_dashboard_summary(self) -> dict:
        items = self.repo.list_items()
        outfits = self.repo.list_outfits()
        low_stock_count = sum(1 for item in items if item.stock_qty <= 5)
        summary = DashboardSummary(
            items_total=len(items),
            outfits_total=len(outfits),
            low_stock_count=low_stock_count,
        )
        return summary.model_dump()

    def get_dashboard_top3(self) -> dict:
        outfits = sorted(
            self.repo.list_outfits(),
            key=lambda o: (o.score if o.score is not None else -1.0, o.created_at),
            reverse=True,
        )
        data = [
            {
                "outfit_id": outfit.outfit_id,
                "title": outfit.title,
                "score": outfit.score,
                "tpo": outfit.tpo.value,
            }
            for outfit in outfits[:3]
        ]
        return DashboardTop3(outfits=data).model_dump()

    def get_dashboard_tpo_ratio(self) -> dict:
        outfits = self.repo.list_outfits()
        if not outfits:
            return DashboardTpoRatio(tpo_ratio={}).model_dump()

        counter = Counter([outfit.tpo.value for outfit in outfits])
        total = len(outfits)
        ratio = {key: round(value / total, 4) for key, value in sorted(counter.items())}
        return DashboardTpoRatio(tpo_ratio=ratio).model_dump()

    def get_dashboard_low_stock(self) -> dict:
        items = sorted(
            [item for item in self.repo.list_items() if item.stock_qty <= 5],
            key=lambda i: (i.stock_qty, i.item_id),
        )
        data = [
            {
                "item_id": item.item_id,
                "category": item.category,
                "sub_category": item.sub_category,
                "stock_qty": item.stock_qty,
            }
            for item in items[:20]
        ]
        return DashboardLowStock(items=data).model_dump()
