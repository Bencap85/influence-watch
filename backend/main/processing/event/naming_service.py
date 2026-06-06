from sqlalchemy.orm import Session
from shared.db.entity.event import Event
from main.processing.event.naming_model import NamingModel
from shared.repository.event_repo import EventRepo


class NamingService:

    def __init__(self, event_repo: EventRepo, naming_model: NamingModel):
        self.event_repo=event_repo
        self.naming_model=naming_model

    def batch_generate_titles(self, db: Session, events: list[Event]) -> dict[str, str]:
        event_to_headlines = {}
        for event in events:
            headlines = self.event_repo.load_n_headlines(db, event.id, n=5)
            event_to_headlines[event.id] = headlines
        
        event_to_title = self.naming_model.generate_event_titles(event_to_headlines)
        return event_to_title