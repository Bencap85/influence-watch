from typing import Dict, List

from shared.db.connect import SessionLocal
from shared.db.entity import EventArticle, ProcessedArticle

def get_articles_for_event_by_country(event_id: str, country: str) -> Dict[str, List[str]]:
    with SessionLocal() as db:
        links = db.query(EventArticle).filter(EventArticle.event_id == event_id).all()
        article_ids = [l.article_id for l in links]

        articles = (
            db.query(ProcessedArticle)
            .filter(ProcessedArticle.article_id.in_(article_ids))
            .filter(ProcessedArticle.country == country)
            .all()
        )

        return {
            "event_id": event_id,
            "articles": [
                {
                    "article_id": a.article_id,
                    "title": a.title,
                    "clean_description_text": a.clean_description_text,
                    "clean_body_text": a.clean_body_text,
                    "sentiment_score": a.sentiment_score,
                    "keyword_list": a.keyword_list,
                    "entity_list": a.entity_list,
                    "country": a.country, 
                    "published_at": a.published_at.isoformat()
                }
                for a in articles
            ],
        }
