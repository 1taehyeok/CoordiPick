from __future__ import annotations

from app.models.api import GenerateRecommendationRequest
from app.models.domain import ComposedRecommendation


class Reranker:
    def rerank(self, recommendations: list[ComposedRecommendation], request: GenerateRecommendationRequest) -> list[ComposedRecommendation]:
        if not request.mood:
            return sorted(recommendations, key=lambda value: value.score, reverse=True)[:6]

        def mood_boost(rec: ComposedRecommendation) -> float:
            return 0.3 if "mood_match" in rec.reason_tags else 0.0

        return sorted(
            recommendations,
            key=lambda value: (value.score + mood_boost(value), value.total_price_krw * -0.00001),
            reverse=True,
        )[:6]
