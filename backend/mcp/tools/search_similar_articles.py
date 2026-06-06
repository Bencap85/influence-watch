from typing import Any, Dict
import uuid

from shared.db.connect import SessionLocal
from sqlalchemy import text

def search_similar_articles(article_id: uuid.UUID, limit: int = 5) -> Dict[str, Any]:
    with SessionLocal() as db:
        embedding = db.execute(
            text("SELECT embedding FROM processed_article WHERE article_id = :id"),
            {"id": article_id}
        ).scalar_one()

        sql = text("""
            SELECT 
                pa.article_id,
                pa.title,
                pa.embedding <=> :embedding AS distance
            FROM processed_article pa
            WHERE pa.article_id != :id
            ORDER BY pa.embedding <=> :embedding
            LIMIT :limit
        """)

        rows = db.execute(sql, {"embedding": embedding, "limit": limit}).fetchall()

        return {
            "results": [
                {
                    "article_id": r.article_id,
                    "title": r.title,
                    "distance": r.distance,
                }
                for r in rows
            ]
        }
