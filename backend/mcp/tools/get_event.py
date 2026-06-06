from shared.db.connect import SessionLocal
from shared.db.entity import Event

def get_event(event_id: str) -> dict:
    with SessionLocal() as db:
        ev = db.query(Event).filter(Event.id == event_id).first()

        if not ev:
            return {"error": "not_found"}

        return {
            "event_id": ev.id,
            "title": ev.title,
            "event_summary": ev.event_summary,
            "global_keywords": ev.global_keywords,
            "global_entities": ev.global_entities,
            "global_sentiment": ev.global_sentiment,
            "countries": ev.countries,
            "num_articles": ev.num_articles,
            "first_seen_at": ev.first_seen_at.isoformat() if ev.first_seen_at else None,
            "last_seen_at": ev.last_seen_at.isoformat() if ev.last_seen_at else None,
        }
