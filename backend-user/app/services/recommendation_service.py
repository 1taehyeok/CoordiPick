from __future__ import annotations

from datetime import datetime, timezone

from app.core.errors import AppError, NotFoundError
from app.models.api import (
    GenerateRecommendationRequest,
    OutfitItem,
    RecommendationCard,
    RecommendationDetailData,
    RecommendationDetailResponse,
    RecommendationListData,
    RecommendationListMeta,
    RecommendationListResponse,
)
from app.recommendation.candidate import CandidateSelector
from app.recommendation.compose import Composer
from app.recommendation.rerank import Reranker
from app.recommendation.scoring import ScoringEngine
from app.repositories.catalog_repository import CatalogRepository
from app.repositories.recommendation_repository import RecommendationRepository


class RecommendationService:
    def __init__(
        self,
        catalog_repository: CatalogRepository,
        recommendation_repository: RecommendationRepository,
        candidate_selector: CandidateSelector,
        scoring_engine: ScoringEngine,
        composer: Composer,
        reranker: Reranker,
    ) -> None:
        self._catalog_repository = catalog_repository
        self._recommendation_repository = recommendation_repository
        self._candidate_selector = candidate_selector
        self._scoring_engine = scoring_engine
        self._composer = composer
        self._reranker = reranker

    def generate(self, request: GenerateRecommendationRequest) -> RecommendationListResponse:
        candidates = self._candidate_selector.select(self._catalog_repository.list_active_items(), request)
        scored = self._scoring_engine.score(candidates, request)
        composed = self._composer.compose(scored, request, limit=6)
        reranked = self._reranker.rerank(composed, request)

        if not reranked:
            raise AppError(
                status_code=400,
                code="INSUFFICIENT_CANDIDATES",
                message="could not compose recommendation set",
            )

        self._recommendation_repository.upsert_many(reranked)
        cards = [
            RecommendationCard(
                recommendation_id=rec.recommendation_id,
                title=rec.title,
                subtitle=rec.subtitle,
                total_price_krw=rec.total_price_krw,
                thumbnail_url=rec.thumbnail_url,
                reason_tags=rec.reason_tags,
            )
            for rec in reranked
        ]
        return RecommendationListResponse(
            success=True,
            data=RecommendationListData(cards=cards),
            meta=RecommendationListMeta(generated_at=datetime.now(timezone.utc)),
        )

    def get_detail(self, recommendation_id: str) -> RecommendationDetailResponse:
        recommendation = self._recommendation_repository.get(recommendation_id)
        if recommendation is None:
            raise NotFoundError(
                message="recommendation not found",
                details={"recommendation_id": recommendation_id},
            )

        items = [
            OutfitItem(
                item_id=item.item_id,
                name=item.name,
                slot=item.slot,
                price_krw=item.price_krw,
                location_zone=item.location_zone,
                image_url=item.image_url,
            )
            for item in recommendation.items
        ]

        return RecommendationDetailResponse(
            success=True,
            data=RecommendationDetailData(
                recommendation_id=recommendation.recommendation_id,
                title=recommendation.title,
                subtitle=recommendation.subtitle,
                total_price_krw=recommendation.total_price_krw,
                items=items,
            ),
        )
