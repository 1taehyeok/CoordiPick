from enum import Enum


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"


class TpoEnum(str, Enum):
    COMMUTE = "commute"
    DATE = "date"
    FRIENDS = "friends"
    TRAVEL = "travel"
    DAILY = "daily"
    SPECIAL = "special"


class SlotEnum(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"
    OUTER = "outer"
    SHOES = "shoes"
    ACC = "acc"


class EventTypeEnum(str, Enum):
    IMPRESSION = "impression"
    CLICK = "click"
    DETAIL_VIEW = "detail_view"


class GenerationSourceEnum(str, Enum):
    RULE = "rule"
    AI = "ai"
    ADMIN = "admin"
