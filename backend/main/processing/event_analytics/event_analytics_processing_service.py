from collections import Counter
import logging
from typing import Dict, List
import uuid
from shared.repository.processed_article_repo import ProcessedArticleRepo
from shared.db.session import SessionLocal
from shared.db.entity import EventAnalytics, Event, ProcessedArticle

class EventAnalyticsProcessingService:

    def __init__(self, processed_article_repo: ProcessedArticleRepo):
        self.processed_article_repo = processed_article_repo
        self.logger = logging.getLogger(__name__)

    def build_event_analytics(self, event_ids: List[uuid.UUID]) -> List[uuid.UUID]:
        with SessionLocal() as db:
            event_analytics = []
            try:
                events = db.query(Event).filter(Event.id.in_(event_ids)).all()

                self.logger.info(f"Found {len(events)} events to build analytics for")
                for idx, event in enumerate(events):
                    self.logger.info(f"Generating event analytics for {idx + 1}/{len(events)}")
                    
                    articles = self.processed_article_repo.get_articles_for_event(db, event.id)
                    self.logger.info(f"Found {len(articles)} articles for event_id: {event.id}")
                    
                    country_to_articles = self._build_country_to_articles(articles)

                    country_embeddings = self._compute_country_embeddings(country_to_articles)
                    country_keywords = self._compute_country_keywords(country_to_articles)
                    country_entities = self._compute_country_entities(country_to_articles)
                    country_sentiment = self._compute_country_sentiment(country_to_articles)

                    global_baseline_embedding = self._compute_global_baseline_embedding(articles)
                    global_baseline_keywords = self._compute_global_baseline_keywords(articles)
                    global_baseline_entities = self._compute_global_baseline_entities(articles)
                    global_baseline_sentiment = self._compute_global_baseline_sentiment(articles)

                    existing = db.get(EventAnalytics, event.id)

                    if existing:
                        existing.country_embeddings = country_embeddings
                        existing.country_keywords = country_keywords
                        existing.country_entities = country_entities
                        existing.country_sentiment = country_sentiment
                        existing.global_baseline_embedding = global_baseline_embedding
                        existing.global_baseline_keywords = global_baseline_keywords
                        existing.global_baseline_entities = global_baseline_entities
                        existing.global_baseline_sentiment = global_baseline_sentiment

                        analytics = existing
                    else:
                        analytics = EventAnalytics(
                            event_id=event.id,
                            country_embeddings=country_embeddings,
                            country_keywords=country_keywords,
                            country_entities=country_entities,
                            country_sentiment=country_sentiment,
                            global_baseline_embedding=global_baseline_embedding,
                            global_baseline_keywords=global_baseline_keywords,
                            global_baseline_entities=global_baseline_entities,
                            global_baseline_sentiment=global_baseline_sentiment
                        )
                        db.add(analytics)

                    event_analytics.append(analytics)

            except Exception as e:
                self.logger.error(e)
                raise e

            db.commit()
            return [ea.event_id for ea in event_analytics]
    
    def _build_country_to_articles(self, articles: List[ProcessedArticle]) -> Dict[str, List[ProcessedArticle]]:
        country_to_articles = {}

        for article in articles:
            if article.country not in country_to_articles:
                country_to_articles[article.country] = []

            country_to_articles[article.country].append(article)

        return country_to_articles
    
    def _compute_country_embeddings(self, country_to_articles: Dict[str, List[ProcessedArticle]]) -> Dict[str, List[float]]:
        result = {}
        for country, articles in country_to_articles.items():
            vectors = [a.embedding for a in articles]
            centroid = sum(vectors) / len(vectors)
            result[country] = centroid.tolist()
        return result
    
    def _compute_country_keywords(self, country_to_articles: Dict[str, List[ProcessedArticle]]) -> Dict[str, List[float]]:
        result = {}
        for country, articles in country_to_articles.items():
            all_keywords = []
            for a in articles:
                if a.keyword_list:
                    all_keywords.extend(a.keyword_list)
            result[country] = [kw for kw, _ in Counter(all_keywords).most_common(30)]
        return result

    def _compute_country_entities(self, country_to_articles: Dict[str, List[ProcessedArticle]]) -> Dict[str, List]:
        result = {}
        for country, articles in country_to_articles.items():
            all_entities = []
            for a in articles:
                if a.entity_list:
                    all_entities.extend([ent[0] for ent in a.entity_list])
            result[country] = [
                {"entity": ent, "count": count}
                for ent, count in Counter(all_entities).most_common(50)
            ]
        return result

    def _compute_country_sentiment(self, country_to_articles: Dict[str, List[ProcessedArticle]]) -> Dict[str, float]:
        result = {}
        for country, articles in country_to_articles.items():
            sentiments = [a.sentiment_score for a in articles if a.sentiment_score is not None]
            result[country] = sum(sentiments) / len(sentiments) if sentiments else 0.0
        return result
    
    def _compute_global_baseline_embedding(self, articles: List[ProcessedArticle]) -> List[float]:
        vectors = [a.embedding for a in articles if a.embedding is not None]
        if not vectors:
            return [0.0] * 1536
        centroid = sum(vectors) / len(vectors)
        return centroid.tolist()
    
    def _compute_global_baseline_keywords(self, articles: List[ProcessedArticle]) -> List[str]:
        all_keywords = []
        for a in articles:
            if a.keyword_list:
                all_keywords.extend(a.keyword_list)

        counter = Counter(all_keywords)
        return [kw for kw, _ in counter.most_common(50)]
    
    def _compute_global_baseline_entities(self, articles: List[ProcessedArticle]) -> List[Dict[str, int]]:
        all_entities = []
        for a in articles:
            if a.entity_list:
                all_entities.extend([ent[0] for ent in a.entity_list])

        counter = Counter(all_entities)
        return [
            {"entity": ent, "count": count}
            for ent, count in counter.most_common(100)
        ]
    
    def _compute_global_baseline_sentiment(self, articles: List[ProcessedArticle]) -> float:
        sentiments = [a.sentiment_score for a in articles if a.sentiment_score is not None]
        if not sentiments:
            return 0.0
        return sum(sentiments) / len(sentiments)




    
                