from typing import List
import uuid

from fastapi import APIRouter, HTTPException
from shared.db.session import SessionLocal
from shared.repository import EventRepo
from .schemas import EventResponse

router = APIRouter(prefix="/events", tags=["events"])
event_repo =  EventRepo()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: str):
    with SessionLocal() as db:
        event = event_repo.get_by_id(db, uuid.UUID(event_id))

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        return event
    
@router.get("/", response_model=List[EventResponse])
def get_all_events():
    with SessionLocal() as db:
        events = event_repo.get_events(db)

        if not events:
            raise HTTPException(status_code=404, detail="No events found")

        return events