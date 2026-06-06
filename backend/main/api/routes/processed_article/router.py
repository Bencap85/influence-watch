from typing import List, Optional
import uuid

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from shared.repository import ProcessedArticleRepo
from shared.db.session import SessionLocal
from shared.db.entity import ProcessedArticle
from .schemas import ProcessedArticleResponse


router = APIRouter(prefix="/articles", tags=["articles"])
processed_article_repo = ProcessedArticleRepo()


@router.get("/{article_id}", response_model=ProcessedArticleResponse)
def get_processed_article(article_id: str):
    with SessionLocal() as db:
        article = processed_article_repo.get_article_by_id(uuid.UUID(article_id), db)

        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        return article

@router.get("", response_model=List[ProcessedArticleResponse])
def get_processed_articles(event_id: Optional[uuid.UUID] = Query(None)):
    with SessionLocal() as db:

        articles = []

        if event_id:
            articles = processed_article_repo.get_articles_for_event(db, event_id)
            if not articles:
                raise HTTPException(status_code=404, detail=f"No articles found for event {event_id}")

        else:
            articles = processed_article_repo.get_articles(db)
            if not articles:
                raise HTTPException(status_code=404, detail=f"No articles found")

        return articles
