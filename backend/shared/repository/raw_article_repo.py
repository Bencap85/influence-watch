from typing import List

from sqlalchemy.orm import Session
from shared.db.entity import RawArticle

class RawArticleRepo():
    
    def get_all(self, db: Session) -> List[RawArticle]:
        return db.query(RawArticle).all()
    
    def save(self, db: Session, RawArticle: RawArticle) -> RawArticle:
        db.add(RawArticle)
        db.commit()
        return RawArticle
    
    def get_by_url(self, db: Session, url: str) -> RawArticle | None:
        return db.query(RawArticle).filter(RawArticle.source_url == url).first()
    
    def get_unprocessed_raw_articles(self, db: Session) -> List[RawArticle]:
        return db.query(RawArticle).filter(RawArticle.is_processed == False).all()
    
    def mark_raw_articles_as_processed(
        self, db: Session, articles: List[RawArticle]
    ) -> None:
        for article in articles:
            article.is_processed = True
            db.add(article)
        db.commit()