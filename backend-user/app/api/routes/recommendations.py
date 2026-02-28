from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.api import (
    GenerateRecommendationRequest,
    RecommendationDetailResponse,
    RecommendationListResponse,
)
from app.services.dependencies import get_recommendation_service
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/generate", response_model=RecommendationListResponse, status_code=200)
def generate_recommendations(
    request: GenerateRecommendationRequest,
    service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendationListResponse:
    return service.generate(request)


@router.get("/{recommendation_id}", response_model=RecommendationDetailResponse, status_code=200)
def get_recommendation_detail(
    recommendation_id: str,
    service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendationDetailResponse:
    return service.get_detail(recommendation_id)
