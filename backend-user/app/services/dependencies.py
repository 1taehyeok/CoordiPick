from __future__ import annotations

from functools import lru_cache

from app.recommendation.candidate import CandidateSelector
from app.recommendation.compose import Composer
from app.recommendation.rerank import Reranker
from app.recommendation.scoring import ScoringEngine
from app.repositories.catalog_repository import CatalogRepository
from app.repositories.event_repository import EventRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.event_service import EventService
from app.services.recommendation_service import RecommendationService


@lru_cache
def get_catalog_repository() -> CatalogRepository:
    return CatalogRepository()


@lru_cache
def get_recommendation_repository() -> RecommendationRepository:
    return RecommendationRepository()


@lru_cache
def get_event_repository() -> EventRepository:
    return EventRepository()


@lru_cache
def get_recommendation_service() -> RecommendationService:
    return RecommendationService(
        catalog_repository=get_catalog_repository(),
        recommendation_repository=get_recommendation_repository(),
        candidate_selector=CandidateSelector(),
        scoring_engine=ScoringEngine(),
        composer=Composer(),
        reranker=Reranker(),
    )


@lru_cache
def get_event_service() -> EventService:
    return EventService(repository=get_event_repository())
