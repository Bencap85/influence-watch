from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from typing import List
from sqlalchemy.orm import Session
from shared.repository.raw_article_repo import RawArticleRepo
from shared.db.entity.raw_article import RawArticle
from shared.db.entity.source import Source
from shared.db.session import SessionLocal
from main.ingestion.rss_client import RSSClient
from main.ingestion.schemas import RSSArticle
from main.ingestion.article_service import ArticleService

class ArticleIngestionService:

    def __init__(
            self, 
            repo: RawArticleRepo, 
            rss_client: RSSClient, 
            article_service: ArticleService,
            should_save_content: bool = False):
        self.repo = repo
        self.rss_client = rss_client
        self.article_service = article_service
        self.should_save_content = should_save_content
        self.logger = logging.getLogger(__name__)

    def dedup_articles(self, db: Session, articles: List[RSSArticle]) -> List[RSSArticle]:
        unique = []
        seen_urls = set([])
        for article in articles:
            if self.repo.get_by_url(db, article.url) or article.url in seen_urls:
                self.logger.info(f"Skipping duplicate: {article.url}")
            else:
                unique.append(article)
                seen_urls.add(article.url)

        return unique
    
    def persist_articles(self, db: Session, articles: List[RSSArticle]):
        for rss_article in articles:
            # Build entity
            entity: RawArticle = self.article_service.build_article_entity(rss_article)

            # Persist
            self.repo.save(db, entity)

    def ingest_sources(self, sources: List[Source]) -> int:
        articles = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_source = {
                executor.submit(self.rss_client.fetch_feed, source): source
                for source in sources
            }

            for future in as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    rss_articles = future.result()
                    articles.extend(rss_articles)
                except Exception as e:
                    self.logger.error(f"Error ingesting {source.base_url}: {e}")

        with SessionLocal() as db:
            try:
                articles = self.dedup_articles(db, articles)
                self.persist_articles(db, articles)
                db.commit()

            except Exception as e:
                db.rollback()
                raise

        return len(articles)
