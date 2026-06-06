import logging
from shared.db.session import SessionLocal
from shared.repository.raw_article_repo import RawArticleRepo
from main.ingestion.schemas import RSSArticle
from main.ingestion.rss_client import RSSClient
from main.ingestion.article_service import ArticleService
from main.ingestion.ingestion_service import ArticleIngestionService
from shared.repository.source_repo import SourceRepo


logger = logging.getLogger(__name__)

def load_sources():
    source_repo = SourceRepo()
    with SessionLocal() as db:
        return source_repo.get_all(db)

def main():
    logger.info("Starting ingestion process...")
    sources = load_sources()

    service = ArticleIngestionService(
        repo=RawArticleRepo(),
        rss_client=RSSClient(),
        article_service=ArticleService()
    )

    total_articles_ingested = service.ingest_sources(sources)

    logger.info(f"Finished ingesting {total_articles_ingested} articles from {len(sources)} sources")
    
if __name__ == "__main__":
    main()