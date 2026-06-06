from __future__ import annotations
from typing import Optional
import numpy as np
import logging
from sqlalchemy.orm import Session
from main.processing.vector_utils import cosine_similarity, normalize_vector
from shared.db.entity.processed_article import ProcessedArticle
from shared.db.entity.event import Event
from shared.repository.event_repo import EventRepo


class ClusteringService:

    def __init__(
            self, 
            event_repo: EventRepo
        ) -> None:
        self.event_repo = event_repo
        self.logger = logging.getLogger(__name__)

    def assign(
        self,
        db: Session,
        article: ProcessedArticle,
        embedding: list[float],
        threshold: float = 0.65
    ) -> Event:
        
        self.logger.info(f"Clustering article: {article.title}")

        nearest = self.event_repo.find_nearest(db, embedding)

        # No events exist → create first event
        if not nearest:
            self.logger.info(f"  - No events exist! Creating first event...")
            event = Event(
                title=None,
                event_summary="",
                centroid_embedding=embedding,
                countries=[article.country],
                global_keywords=[],
                global_entities=[],
                global_sentiment=0.0,
                first_seen_at=article.processed_at,
                last_seen_at=article.processed_at
            )
            event = self.event_repo.save(db, event)
            self.event_repo.add_article_to_event(db, article.article_id, event.id)
            return event
        
        self.logger.info(f"  - Nearest event is {nearest['title']}")

        # Compute similarity
        centroid = np.array(nearest["centroid_embedding"])
        score = cosine_similarity(
            normalize_vector(embedding), 
            normalize_vector(centroid.tolist())
        )

        self.logger.info(f"  - Cosine similarity score: {score}")

        # Too different → create new event
        if score < threshold:
            self.logger.info(f"  - Too different. Creating new event...")
            event = event = Event(
                title=None,
                event_summary="",
                centroid_embedding=embedding,
                global_keywords=[],
                global_entities=[],
                global_sentiment=0.0,
                countries=[article.country],
                num_articles=1,
                first_seen_at=article.processed_at,
                last_seen_at=article.processed_at
            )
            event = self.event_repo.save(db, event)
            self.event_repo.add_article_to_event(db, article.article_id, event.id)
            return event
        else:
            self.logger.info(f"  - Clustered into event: {nearest['title']}")

        # Assign to existing event
        event = self.event_repo.get_by_id(db, nearest["id"])
        assert event is not None

        self.event_repo.add_article_to_event(db, article.article_id, event.id)

        # Update centroid
        old = np.array(event.centroid_embedding)
        count = event.num_articles
        event.centroid_embedding = ((old * count) + embedding) / (count + 1)

        # Update metadata
        # event.num_articles += 1   
        # if article.country not in event.countries:
        #     event.countries = event.countries + [article.country]
        # if not event.last_seen_at or (article.published_at and article.published_at > event.last_seen_at):
        #     event.last_seen_at = article.published_at
        # if not event.first_seen_at or (article.published_at and article.published_at < event.first_seen_at):
        #     event.first_seen_at = article.published_at

        # Save updated metadata
        self.event_repo.save(db, event)
        return event
