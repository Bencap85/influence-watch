from datetime import datetime
import logging
import uuid
from sqlalchemy import desc
from shared.db.entity.processed_article import ProcessedArticle
import numpy as np
from sqlalchemy import text
from sqlalchemy.orm import Session
from shared.db.entity.event_article import EventArticle
from shared.db.entity.event import Event


class EventRepo:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def find_nearest(self, db: Session, embedding: np.ndarray | list[float], limit: int=1): 

        if isinstance(embedding, np.ndarray): 
            embedding = embedding.tolist()

        sql = text(
            """ 
            SELECT id, title, centroid_embedding
            FROM event 
            ORDER BY centroid_embedding <=> (:embedding)::vector 
            LIMIT :limit 
            """) 
        row = db.execute(sql, {"embedding": embedding, "limit": limit}).mappings().fetchone() 
        return row
    
    def update_event_centroid(self, db: Session, event_id: int, new_vec: np.ndarray):
        count = db.query(EventArticle).filter_by(event_id=event_id).count()
        event = db.query(Event).filter_by(id=event_id).first()
        if event is None:
            self.logger.info(f"Unable to find event for id: {event_id}!")
            return

        if count <= 1:
            event.centroid_embedding = new_vec 
            return
        
        old = np.array(event.centroid_embedding)
        updated = (old * (count - 1) + new_vec) / count
        event.centroid_embedding = updated.tolist()

    def update_event_countries(self, db: Session, event_id: int, country_code: str):
        event = db.query(Event).filter_by(id=event_id).first()
        if event is None:
            self.logger.info(f"Unable to find event for id: {event_id}!")
            return
        if not event.countries:
            event.countries = []
        if country_code not in event.countries:
            event.countries = event.countries + [country_code]
        db.flush()

    def update_event_article_count(self, db: Session, event_id: int):
        event = db.query(Event).filter_by(id=event_id).first()
        if event is None:
            self.logger.info(f"Unable to find event for id: {event_id}!")
            return
        event.num_articles += 1

    def update_event_last_seen(self, db: Session, event_id: int, pub_date: datetime):
        event = db.query(Event).filter_by(id=event_id).first()
        if event is None:
            self.logger.info(f"Unable to find event for id: {event_id}!")
            return
    
        if not pub_date or not event.last_seen_at or pub_date >= event.last_seen_at:
            event.last_seen_at = pub_date

    def save(self, db: Session, event: Event) -> Event:
        db.add(event)
        db.flush()
        db.refresh(event)
        return event
    
    def get_by_id(self, db: Session, event_id: uuid.UUID) -> Event | None:
        return db.query(Event).filter(Event.id == event_id).first()
    
    def add_article_to_event(self, db: Session, article_id: uuid.UUID, event_id: uuid.UUID) -> EventArticle:
        article_event = EventArticle(article_id=article_id, event_id=event_id)
        db.add(article_event)
        db.commit()
        return article_event
    
    def get_unnamed_events(self, db: Session) -> list[Event]:
        events = db.query(Event).filter( 
            (Event.title.is_(None)) | (Event.title == '')
        ).all()
        return events
    
    def load_n_headlines(self, db: Session, event_id: uuid.UUID, n: int=5) -> list[str | None]:
        rows = (
            db.query(ProcessedArticle)
                .join(EventArticle, EventArticle.article_id == ProcessedArticle.article_id)
                .filter(EventArticle.event_id == event_id)
                .limit(n)
                .all()
        )
        headlines = [row.title for row in rows]
        return headlines

    def update_event_title(self, db: Session, event_id: uuid.UUID, title: str) -> Event | None:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event is None:
            self.logger.info(f"Unable to find event for id: {event_id}!")
            return
        event.title = title
        db.merge(event)
        return event
    
    def get_events(self, db: Session) -> list[Event]:
        return db.query(Event).order_by(desc(Event.num_articles)).all()
    
    def get_event_for_article(self, db: Session, article_id: int) -> Event | None:
        return (
            db.query(Event)
            .join(EventArticle, EventArticle.event_id == Event.id)
            .join(ProcessedArticle, ProcessedArticle.article_id == EventArticle.article_id)
            .filter(ProcessedArticle.article_id == article_id)
            .first()
        )

    