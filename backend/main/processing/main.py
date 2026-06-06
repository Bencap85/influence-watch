from multiprocessing import Process

from main.processing.detection.detection_processing_service import DetectionProcessingService
from main.processing.event_analytics.event_analytics_processing_service import EventAnalyticsProcessingService
from main.processing.article.entity_service import EntityService
from main.processing.article.keyword_service import KeywordService
from main.processing.article.sentiment_service import SentimentService
from main.processing.event.event_processing_service import EventProcessingService
from main.processing.event.naming_model import NamingModel
from main.processing.event.naming_service import NamingService
from shared.repository.detection_repo import DetectionRepo
from shared.repository.event_repo import EventRepo
from main.processing.event.clustering_service import ClusteringService
from main.processing.embedding_client import EmbeddingClient
from shared.repository.processed_article_repo import ProcessedArticleRepo
from main.processing.article.article_processing_service import ArticleProcessingService
from shared.db.session import SessionLocal
from shared.repository.raw_article_repo import RawArticleRepo
import logging

logger = logging.getLogger(__name__)

def main():

    article_processing_service = ArticleProcessingService(
        raw_article_repo=RawArticleRepo(), 
        processed_article_repo=ProcessedArticleRepo(),
        embedding_client=EmbeddingClient(),
        clustering_service=ClusteringService(EventRepo()),
        sentiment_service=SentimentService(),
        keyword_service=KeywordService(),
        entity_service=EntityService()
    )

    event_processing_service = EventProcessingService(
        event_repo=EventRepo(),
        processed_article_repo=ProcessedArticleRepo(),
        clustering_service=ClusteringService(
            event_repo=EventRepo()
        ),
        naming_service=NamingService(
            event_repo=EventRepo(),
            naming_model=NamingModel()
        )
    )

    event_analytics_processing_service = EventAnalyticsProcessingService(
        processed_article_repo=ProcessedArticleRepo()
    )
    
    detection_processing_service = DetectionProcessingService(
        processed_article_repo=ProcessedArticleRepo(),
        detection_repo=DetectionRepo()
    )
    
    ### Begin Processing ###

    article_processing_service.process_raw_articles()

    logger.info("Completed processing articles. Building events now...")
    event_ids = event_processing_service.build_events()
 
    logger.info("Enriching events...")
    event_ids = event_processing_service.enrich_events(event_ids)

    logger.info("Naming events...")
    event_ids = event_processing_service.name_events(event_ids)

    logger.info("Populating event_analytics now...")
    event_ids = event_analytics_processing_service.build_event_analytics(event_ids)

    logger.info("Building detections...")
    detections = detection_processing_service.generate_detections(event_ids)

if __name__ == "__main__":
    main()