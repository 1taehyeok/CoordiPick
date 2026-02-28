from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.api import CreateEventRequest, EnvelopeSimpleResponse
from app.services.dependencies import get_event_service
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EnvelopeSimpleResponse, status_code=201)
def create_event(
    request: CreateEventRequest,
    service: EventService = Depends(get_event_service),
) -> EnvelopeSimpleResponse:
    return service.create(request)
