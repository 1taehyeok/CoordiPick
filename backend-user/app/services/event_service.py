from __future__ import annotations

from app.models.api import CreateEventRequest, EnvelopeSimpleResponse
from app.repositories.event_repository import EventRepository


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self._repository = repository

    def create(self, request: CreateEventRequest) -> EnvelopeSimpleResponse:
        event = self._repository.create(
            session_id=request.session_id,
            event_type=request.event_type.value,
            recommendation_id=request.recommendation_id,
            payload=request.payload or {},
        )
        return EnvelopeSimpleResponse(
            success=True,
            data={
                "event_id": event.event_id,
            },
        )
