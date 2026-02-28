from functools import lru_cache

from app.repositories.memory import InMemoryAdminRepository
from app.services.admin_service import AdminService


@lru_cache
def get_admin_repository() -> InMemoryAdminRepository:
    return InMemoryAdminRepository()


def get_admin_service() -> AdminService:
    return AdminService(get_admin_repository())


def reset_dependencies() -> None:
    get_admin_repository().reset()
