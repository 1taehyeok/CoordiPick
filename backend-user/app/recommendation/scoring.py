from __future__ import annotations

from app.models.api import GenerateRecommendationRequest
from app.models.domain import Item, ScoredItem


class ScoringEngine:
    def score(self, candidates: list[Item], request: GenerateRecommendationRequest) -> list[ScoredItem]:
        scored: list[ScoredItem] = []
        for item in candidates:
            score = 1.0
            reason_tags: list[str] = ["tpo_match", "temp_fit"]

            if request.mood and request.mood in item.moods:
                score += 0.5
                reason_tags.append("mood_match")

            center = (item.temperature_min + item.temperature_max) / 2
            temp_distance = abs(center - request.temperature_c)
            score += max(0.0, 1.0 - temp_distance / 20.0)
            score += 0.2 if item.gender == request.gender.value else 0.1

            scored.append(ScoredItem(item=item, score=score, reason_tags=reason_tags))

        return sorted(scored, key=lambda value: value.score, reverse=True)
