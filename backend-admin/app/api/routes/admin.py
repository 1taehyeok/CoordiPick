from fastapi import APIRouter, Depends, Response, status

from app.core.auth import require_admin_bearer
from app.core.responses import success_response
from app.dependencies import get_admin_service
from app.models.admin import (
    ItemCreate,
    ItemUpdate,
    OutfitCreate,
    OutfitUpdate,
    StoreSettingsUpdate,
)
from app.services.admin_service import AdminService

router = APIRouter(
    tags=["admin"],
    dependencies=[Depends(require_admin_bearer)],
)


@router.get("/admin/items", operation_id="listItems")
def list_items(service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response({"items": service.list_items()})


@router.post("/admin/items", status_code=status.HTTP_201_CREATED, operation_id="createItem")
def create_item(payload: ItemCreate, service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response(service.create_item(payload))


@router.patch("/admin/items/{item_id}", operation_id="updateItem")
def update_item(
    item_id: str,
    payload: ItemUpdate,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    return success_response(service.update_item(item_id, payload))


@router.delete("/admin/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="deleteItem")
def delete_item(item_id: str, service: AdminService = Depends(get_admin_service)) -> Response:
    service.delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/admin/outfits", operation_id="listOutfits")
def list_outfits(service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response({"outfits": service.list_outfits()})


@router.post("/admin/outfits", status_code=status.HTTP_201_CREATED, operation_id="createOutfit")
def create_outfit(payload: OutfitCreate, service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response(service.create_outfit(payload))


@router.patch("/admin/outfits/{outfit_id}", operation_id="updateOutfit")
def update_outfit(
    outfit_id: str,
    payload: OutfitUpdate,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    return success_response(service.update_outfit(outfit_id, payload))


@router.delete(
    "/admin/outfits/{outfit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deleteOutfit",
)
def delete_outfit(outfit_id: str, service: AdminService = Depends(get_admin_service)) -> Response:
    service.delete_outfit(outfit_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/admin/store-settings", operation_id="getStoreSettings")
def get_store_settings(service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response(service.get_store_settings())


@router.patch("/admin/store-settings", operation_id="updateStoreSettings")
def update_store_settings(
    payload: StoreSettingsUpdate,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    return success_response(service.update_store_settings(payload))


@router.get("/admin/dashboard/summary", operation_id="getDashboardSummary")
def get_dashboard_summary(service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response(service.get_dashboard_summary())


@router.get("/admin/dashboard/top3", operation_id="getDashboardTop3")
def get_dashboard_top3(service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response(service.get_dashboard_top3())


@router.get("/admin/dashboard/tpo-ratio", operation_id="getDashboardTpoRatio")
def get_dashboard_tpo_ratio(service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response(service.get_dashboard_tpo_ratio())


@router.get("/admin/dashboard/low-stock", operation_id="getDashboardLowStock")
def get_dashboard_low_stock(service: AdminService = Depends(get_admin_service)) -> dict:
    return success_response(service.get_dashboard_low_stock())
