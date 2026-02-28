from __future__ import annotations

from app.models.domain import Item


class CatalogRepository:
    def __init__(self) -> None:
        self._items = [
            Item("1001", "Breeze Shirt", "top", "male", ["commute", "daily", "travel"], ["clean", "casual"], 10, 27, 59000, "https://img.coordipick.dev/1001.jpg", "A-01"),
            Item("1002", "Slim Slacks", "bottom", "male", ["commute", "date", "daily"], ["clean"], 8, 25, 79000, "https://img.coordipick.dev/1002.jpg", "A-03"),
            Item("1003", "Runner Shoes", "shoes", "unisex", ["commute", "daily", "travel"], ["casual", "sporty"], 0, 30, 89000, "https://img.coordipick.dev/1003.jpg", "S-01"),
            Item("1004", "Light Jacket", "outer", "male", ["commute", "travel", "daily"], ["clean"], 5, 20, 99000, "https://img.coordipick.dev/1004.jpg", "O-02"),
            Item("1005", "Leather Belt", "acc", "unisex", ["commute", "date", "special"], ["clean"], -5, 35, 39000, "https://img.coordipick.dev/1005.jpg", "C-07"),
            Item("2001", "Crop Knit", "top", "female", ["date", "friends", "daily"], ["romantic", "casual"], 7, 21, 69000, "https://img.coordipick.dev/2001.jpg", "B-02"),
            Item("2002", "Pleated Skirt", "bottom", "female", ["date", "friends", "special"], ["romantic"], 5, 22, 82000, "https://img.coordipick.dev/2002.jpg", "B-05"),
            Item("2003", "Mary Jane", "shoes", "female", ["date", "friends", "special"], ["romantic"], 0, 28, 94000, "https://img.coordipick.dev/2003.jpg", "S-03"),
            Item("2004", "Short Trench", "outer", "female", ["commute", "date", "special"], ["clean"], 4, 18, 129000, "https://img.coordipick.dev/2004.jpg", "O-01"),
            Item("2005", "Mini Bag", "acc", "female", ["date", "friends", "special"], ["romantic", "clean"], -3, 30, 73000, "https://img.coordipick.dev/2005.jpg", "C-02"),
            Item("3001", "Oversized Tee", "top", "unisex", ["daily", "travel", "friends"], ["casual", "street"], 12, 35, 45000, "https://img.coordipick.dev/3001.jpg", "A-11"),
            Item("3002", "Wide Denim", "bottom", "unisex", ["daily", "travel", "friends"], ["casual", "street"], 8, 32, 68000, "https://img.coordipick.dev/3002.jpg", "A-09"),
            Item("3003", "Retro Sneaker", "shoes", "unisex", ["daily", "travel", "friends"], ["street"], 2, 35, 97000, "https://img.coordipick.dev/3003.jpg", "S-09"),
        ]

    def list_active_items(self) -> list[Item]:
        return [item for item in self._items if item.is_active]
