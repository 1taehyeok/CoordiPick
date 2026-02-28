from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from app.models.api import GenerateRecommendationRequest
from app.models.domain import ComposedRecommendation, Item, ScoredItem


MANDATORY_SLOTS = ("top", "bottom", "shoes")
OPTIONAL_SLOTS = ("outer", "acc")


class Composer:
    def compose(self, scored_items: list[ScoredItem], request: GenerateRecommendationRequest, limit: int = 6) -> list[ComposedRecommendation]:
        grouped: dict[str, list[ScoredItem]] = defaultdict(list)
        for scored in scored_items:
            grouped[scored.item.slot].append(scored)

        for slot in MANDATORY_SLOTS:
            if not grouped.get(slot):
                return []

        composed: list[ComposedRecommendation] = []
        max_depth = 2
        rec_index = 1

        for top_idx, top in enumerate(grouped["top"][:max_depth]):
            for bottom_idx, bottom in enumerate(grouped["bottom"][:max_depth]):
                for shoes_idx, shoes in enumerate(grouped["shoes"][:max_depth]):
                    if len(composed) >= limit:
                        return composed

                    selected: list[ScoredItem] = [top, bottom, shoes]
                    if grouped.get("outer"):
                        selected.append(grouped["outer"][(top_idx + bottom_idx) % len(grouped["outer"])])
                    if grouped.get("acc"):
                        selected.append(grouped["acc"][(bottom_idx + shoes_idx) % len(grouped["acc"])])

                    items: list[Item] = [entry.item for entry in selected]
                    score = sum(entry.score for entry in selected)
                    reason_tags = sorted({tag for entry in selected for tag in entry.reason_tags})
                    recommendation_id = f"rec_{request.session_id}_{rec_index}"
                    rec_index += 1
                    composed.append(
                        ComposedRecommendation(
                            recommendation_id=recommendation_id,
                            title=f"{request.tpo.value.title()} Outfit #{len(composed) + 1}",
                            subtitle=(f"Mood: {request.mood}" if request.mood else "Balanced for your context"),
                            total_price_krw=sum(item.price_krw for item in items),
                            thumbnail_url=items[0].image_url,
                            reason_tags=reason_tags,
                            items=items,
                            score=score,
                            created_at=datetime.now(timezone.utc),
                        )
                    )

        return composed
