import logging
import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from shared.db.entity import Source
from main.ingestion.schemas import RSSArticle


logger = logging.getLogger(__name__)

def parse_datetime(value):
    if not value:
        return None
    try:
        return parser.parse(value)
    except Exception:
        return None

class RSSClient:

    def fetch_feed(self, source: Source) -> list[RSSArticle]:
        logger.info(f"Fetching articles from {source.name}...")
        feed = feedparser.parse(source.base_url)
        articles = []

        for entry in feed.entries:
            raw_date = (
                entry.get("published") or entry.get("updated") or
                entry.get("created") or entry.get("pubDate")
            )
            published_at = parse_datetime(raw_date)

            articles.append(
                RSSArticle(
                    title=entry.get("title", ""),
                    description=entry.get("description", ""),
                    url=entry.get("link", ""),
                    source_name=source.name,
                    published_at=published_at,
                    content=entry.get("content", [{}])[0].get("value"),
                    source_id=source.id,
                    country_code=source.country_code,
                    is_state_affiliated=source.is_state_affiliated
                )
            )

        logger.info(f"Found {len(articles)} articles from {source.name}")
        return articles

