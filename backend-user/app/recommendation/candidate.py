from __future__ import annotations

from app.models.api import GenerateRecommendationRequest
from app.models.domain import Item


class CandidateSelector:
    def select(self, items: list[Item], request: GenerateRecommendationRequest) -> list[Item]:
        selected: list[Item] = []
        for item in items:
            if not item.is_active:
                continue
            if item.gender not in (request.gender.value, "unisex"):
                continue
            if request.tpo.value not in item.tpos:
                continue
            if not (item.temperature_min <= request.temperature_c <= item.temperature_max):
                continue
            selected.append(item)
        return selected
