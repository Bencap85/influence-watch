from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple
import logging
import uuid
from collections import Counter
from shared.repository.processed_article_repo import ProcessedArticleRepo
from main.processing.event.naming_service import NamingService
from sqlalchemy.orm import Session
from shared.db.session import SessionLocal
from shared.repository.event_repo import EventRepo
from main.processing.event.clustering_service import ClusteringService
from shared.db.entity import Event


class EventProcessingService:

    def __init__(
        self,
        event_repo: EventRepo,
        processed_article_repo: ProcessedArticleRepo,
        clustering_service: ClusteringService,
        naming_service: NamingService
    ) -> None:
        self.event_repo = event_repo
        self.processed_article_repo = processed_article_repo
        self.clustering_service = clustering_service
        self.naming_service = naming_service
        self.logger = logging.getLogger(__name__)

    def build_events(self) -> List[uuid.UUID]:
        with SessionLocal() as db:
            try:
                rows = self.processed_article_repo.load_unclustered_articles(db)
                self.logger.info(f"Clustering {len(rows)} articles...")

                events = []

                for idx, article in enumerate(rows, start=1):
                    self.logger.info(f"Clustering {idx}/{len(rows)}")
                    event = self.clustering_service.assign(
                        db=db,
                        article=article,
                        embedding=article.embedding
                    )
                    events.append(event)

                db.commit()
                return [event.id for event in events]

            except Exception:
                db.rollback()
                raise

    def enrich_events(self, event_ids: List[uuid.UUID]) -> List[uuid.UUID]:
        with SessionLocal() as db:
            try:
                events = db.query(Event).filter(Event.id.in_(event_ids)).all()
                self.logger.info(f"Enriching {len(events)} events...")
                for idx, event in enumerate(events):
                    self.logger.info(f"Enriching event {idx + 1}/{len(events)}")
                    
                    # Fetch all articles related to this event
                    articles = self.processed_article_repo.get_articles_for_event(db, event.id)

                    # Update event metadata
                    countries = list({article.country for article in articles if article.country})
                    num_articles = len(articles)
                    first_seen_at = min(article.published_at for article in articles)
                    last_seen_at = max(article.published_at for article in articles)
                    
                    sentiments = [a.sentiment_score for a in articles if a.sentiment_score is not None]
                    global_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0

                    all_keywords = []
                    for article in articles:
                        if article.keyword_list:
                            all_keywords.extend(article.keyword_list)
                    global_keywords = [kw for kw, _ in Counter(all_keywords).most_common(20)]

                    all_entities = []
                    for article in articles:
                        if article.entity_list:
                            for ent_text, ent_label in article.entity_list:
                                all_entities.append((ent_text, ent_label))
                    counter = Counter([e[0] for e in all_entities])
                    global_entities = [
                        {"entity": ent, "count": count}
                        for ent, count in counter.most_common(50)
                    ]

                    event.countries = countries
                    event.num_articles = num_articles
                    event.first_seen_at = first_seen_at
                    event.last_seen_at = last_seen_at
                    event.global_sentiment = global_sentiment
                    event.global_keywords = global_keywords
                    event.global_entities = global_entities

                db.commit()

            except Exception:
                db.rollback()
                raise

        return event_ids

    def name_events(self, event_ids: List[uuid.UUID], batch_size: int=20) -> List[uuid.UUID]:
        with SessionLocal() as db:
            try:
                events = db.query(Event).filter(Event.id.in_(event_ids)).all()

                self.logger.info(f"Found {len(events)} events to name")
                
                batches = self._generate_batches(events)
                all_names: Dict[str, str] = {}

                with ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_names = {
                        executor.submit(self._name_batch, batch): batch
                        for batch in batches
                    }

                    for future in as_completed(future_to_names):
                        try:
                            batch_names = future.result()
                            all_names.update(batch_names)
                        except Exception as e:
                            self.logger.error(f"Error naming events: {e}")

                self.logger.info(f"Named {len(all_names)} events")

                for event_id, title in all_names.items():
                    try:
                        self.event_repo.update_event_title(db, uuid.UUID(event_id), title)
                    except Exception as e:
                        self.logger.error("Failed to save article title. Skipping for now, will process next run...", e)
                        continue
                    
                db.commit()
                return event_ids

            finally:
                db.close()

    def _name_batch(self, batch: List[Event]) -> Dict[str, str]:
        with SessionLocal() as db:
            event_to_titles = self.naming_service.batch_generate_titles(db, batch)
            return event_to_titles

    def _generate_batches(self, events: List[Event], batch_size: int=20) -> List[List[Event]]:
        batches = []
        buffer = []
        for event in events:

            # Skip events that are already named
            if event.title is not None and event.title != '':
                self.logger.info("Event already named! Skipping...")
                continue
        
            if len(buffer) >= batch_size:
                batches.append(buffer)
                buffer = []
            
            buffer.append(event)

        if buffer:
            batches.append(buffer)

        return batches
