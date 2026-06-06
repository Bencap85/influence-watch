from typing import List
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session
from shared.db.entity.event_article import EventArticle
from shared.db.entity import ProcessedArticle

class ProcessedArticleRepo():
    
    def save_all(self, db: Session, articles: List[ProcessedArticle]) -> List[ProcessedArticle]:
        for article in articles:
            db.add(article)
        db.commit()

        # Refresh objects so they have DB-generated values
        for article in articles:
            db.refresh(article)

        return articles
    
    def save(self, db: Session, article: ProcessedArticle) -> ProcessedArticle:
        db.add(article)
        db.flush()
        db.refresh(article)
        return article
    
    def load_unclustered_articles(self, db: Session) -> List[ProcessedArticle]:
        stmt = (
            select(ProcessedArticle)
            .outerjoin(EventArticle, ProcessedArticle.article_id == EventArticle.article_id)
            .where(EventArticle.article_id.is_(None))
        )
        return list(db.execute(stmt).scalars().all())
    
    def get_articles_for_event(self, db: Session, event_id: uuid.UUID) -> List[ProcessedArticle]:
        return db \
            .query(ProcessedArticle) \
            .filter(EventArticle.event_id == event_id) \
            .join(EventArticle, EventArticle.article_id == ProcessedArticle.article_id) \
            .all()
    
    def get_state_affiliated_articles_for_event(self, db: Session, event_id: uuid.UUID) -> List[ProcessedArticle]:
        return db \
            .query(ProcessedArticle) \
            .filter(EventArticle.event_id == event_id) \
            .filter(ProcessedArticle.is_state_affiliated == True) \
            .join(EventArticle, EventArticle.article_id == ProcessedArticle.article_id) \
            .all()
    
    def get_article_by_id(self, article_id: uuid.UUID, db: Session) -> ProcessedArticle | None:
        return db.query(ProcessedArticle).filter(ProcessedArticle.article_id == article_id).first()
    
    def get_articles(self, db: Session) -> List[ProcessedArticle]:
        return db.query(ProcessedArticle).all()
    