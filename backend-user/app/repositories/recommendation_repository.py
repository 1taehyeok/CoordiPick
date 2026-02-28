from __future__ import annotations

from threading import Lock

from app.models.domain import ComposedRecommendation


class RecommendationRepository:
    def __init__(self) -> None:
        self._items: dict[str, ComposedRecommendation] = {}
        self._lock = Lock()

    def upsert_many(self, recommendations: list[ComposedRecommendation]) -> None:
        with self._lock:
            for recommendation in recommendations:
                self._items[recommendation.recommendation_id] = recommendation

    def get(self, recommendation_id: str) -> ComposedRecommendation | None:
        return self._items.get(recommendation_id)
