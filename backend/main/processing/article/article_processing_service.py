
import logging
from typing import Any, Dict, List
from main.processing.article.entity_service import EntityService
from main.processing.article.keyword_service import KeywordService
from main.processing.article.sentiment_service import SentimentService
from main.processing.event.clustering_service import ClusteringService
from main.processing.embedding_client import EmbeddingClient
from main.processing.text_cleaner import clean_html, strip_metadata
from main.processing.meta_phrases import RT_META_PHRASES
from shared.db.entity.processed_article import ProcessedArticle
from shared.db.entity.raw_article import RawArticle
from shared.repository.processed_article_repo import ProcessedArticleRepo
from shared.repository.raw_article_repo import RawArticleRepo
from shared.db.session import SessionLocal


class ArticleProcessingService:

    def __init__(
            self, 
            raw_article_repo: RawArticleRepo, 
            processed_article_repo: ProcessedArticleRepo,
            embedding_client: EmbeddingClient,
            clustering_service: ClusteringService,
            sentiment_service: SentimentService,
            keyword_service: KeywordService,
            entity_service: EntityService
        ):
        self.raw_article_repo = raw_article_repo
        self.processed_article_repo = processed_article_repo
        self.embedding_client = embedding_client
        self.clustering_service = clustering_service
        self.sentiment_service = sentiment_service
        self.keyword_service = keyword_service
        self.entity_service = entity_service
        self.logger = logging.getLogger(__name__)

    def process_raw_articles(self):
        with SessionLocal() as db:
            self.logger.info("Starting process_raw_articles job...")

            unprocessed = self.raw_article_repo.get_unprocessed_raw_articles(db)
            self.logger.info(f"Found {len(unprocessed)} to process")

            if len(unprocessed) <= 0:
                return

            # generate list of embeddings for articles
            self.logger.info(f"Embedding {len(unprocessed)} articles...")
            embeddings = self.embedding_client.batch_embed_http(
                [f"{article.title} {article.description_text}" for article in unprocessed], self.logger
            )

            # Process each article
            for idx, raw_article in enumerate(unprocessed):
                self.logger.info(f"Processing article {idx + 1} / {len(unprocessed)}...")

                clean_description = clean_html(raw_article.description_text)
                if raw_article.source_name == 'Russia Today - Daily news':
                    clean_description = strip_metadata(clean_description, RT_META_PHRASES)

                clean_body = clean_html(raw_article.body_text)
                if raw_article.source_name == 'Russia Today - Daily news':
                    clean_body = strip_metadata(clean_body, RT_META_PHRASES)

                overrides = {
                    "clean_body_text": clean_body,
                    "clean_description_text": clean_description,
                    "embedding": embeddings[idx],
                    "sentiment_score": self._detect_sentiment(f"{raw_article.title} {clean_description}"),
                    "keyword_list": self._extract_keywords(f"{raw_article.title} {clean_description}"),
                    "entity_list": self._extract_entities(f"{raw_article.title} {clean_description}")
                }

                # Insert processed_article into database, return managed entity
                entity = self._build_processed_article_entity(raw_article, overrides=overrides)
                entity = self.processed_article_repo.save(db, entity)
                
                # Finally, mark raw_article as processed
                self.raw_article_repo.mark_raw_articles_as_processed(db, [raw_article])

            self.logger.info(f"Successfully processed {len(unprocessed)} raw articles")

    def _detect_sentiment(self, text: str) -> float:
        return self.sentiment_service.get_sentiment(text)
    
    def _extract_keywords(self, text: str) -> List[str]:
        return self.keyword_service.get_keywords(text)
    
    def _extract_entities(self, text: str) -> List[str]:
        return self.entity_service.get_entities(text)
    
    def _build_processed_article_entity(
        self,
        raw_article: RawArticle,
        overrides: Dict[str, Any] | None = None
    ) -> ProcessedArticle:

        overrides = overrides or {}

        processed = ProcessedArticle(
            article_id = raw_article.article_id,
            title = raw_article.title,
            clean_body_text = raw_article.body_text,
            clean_description_text = raw_article.body_text,
            summary = None,
            embedding = None,
            sentiment_score = None,
            keyword_list = None,
            entity_list = None,
            country = raw_article.country,
            is_state_affiliated = raw_article.is_state_affiliated,
            published_at = raw_article.published_at,
            source_name = raw_article.source_name
        )

        # Apply overrides dynamically
        for key, value in overrides.items():
            if hasattr(processed, key):
                setattr(processed, key, value)
            else:
                raise AttributeError(
                    f"ProcessedArticle has no attribute '{key}'"
                )

        return processed
