from datetime import datetime

from shared.db.entity import RawArticle
from main.ingestion.schemas import RSSArticle


class ArticleService:

    def build_article_entity(self, rss_article: RSSArticle) -> RawArticle:
        return RawArticle(
            source_id=rss_article.source_id,
            source_url=rss_article.url,
            source_name=rss_article.source_name,
            title=rss_article.title,
            body_text=rss_article.content,
            description_text=rss_article.description,
            language="en",
            published_at=rss_article.published_at or datetime.utcnow(),
            country=rss_article.country_code,
            is_state_affiliated=rss_article.is_state_affiliated
        )
