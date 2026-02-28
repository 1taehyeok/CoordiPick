from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from app.models.domain import Event


class EventRepository:
    def __init__(self) -> None:
        self._events: list[Event] = []
        self._lock = Lock()

    def create(self, session_id: str, event_type: str, recommendation_id: str, payload: dict) -> Event:
        event = Event(
            event_id=f"evt_{uuid4().hex[:12]}",
            session_id=session_id,
            event_type=event_type,
            recommendation_id=recommendation_id,
            payload=payload,
            created_at=datetime.now(timezone.utc),
        )
        with self._lock:
            self._events.append(event)
        return event
