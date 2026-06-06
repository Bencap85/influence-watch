from typing import Any, Dict, List
import uuid
from shared.db.connect import SessionLocal
from sqlalchemy import text

def search_similar_events(event_id: uuid.UUID, limit: int = 5) -> Dict[str, List[Dict[str, Any]]]:
    with SessionLocal() as db:
        embedding = db.execute(
            text("SELECT centroid_embedding FROM event WHERE event_id = :id"),
            {"id": event_id}
        ).scalar_one()

        sql = text("""
            SELECT id, title, centroid_embedding <=> :embedding AS distance
            FROM event
            ORDER BY centroid_embedding <=> :embedding
            LIMIT :limit
        """)

        rows = db.execute(sql, {"embedding": embedding, "limit": limit}).fetchall()

        return {
            "results": [
                {
                    "event_id": r.id,
                    "title": r.title,
                    "distance": r.distance,
                }
                for r in rows
            ]
        }
