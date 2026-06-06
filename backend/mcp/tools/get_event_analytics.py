from shared.db.connect import SessionLocal
from shared.db.entity import EventAnalytics

def get_event_analytics(event_id: str) -> dict:
    with SessionLocal() as db:
        ea = db.query(EventAnalytics).filter(EventAnalytics.event_id == event_id).first()

        if not ea:
            return {"error": "not_found"}

        return {
            "event_id": ea.event_id,
            "country_keywords": ea.country_keywords,
            "country_entities": ea.country_entities,
            "country_sentiment": ea.country_sentiment,
            "global_baseline_keywords": ea.global_baseline_keywords,
            "global_baseline_entities": ea.global_baseline_entities,
            "global_baseline_sentiment": ea.global_baseline_sentiment,
        }
