from shared.config.logging_config import setup_logging

setup_logging()

from shared.repository.event_repo import EventRepo
from shared.repository.processed_article_repo import ProcessedArticleRepo
from shared.repository.raw_article_repo import RawArticleRepo
from shared.repository.source_repo import SourceRepo
from shared.repository.detection_repo import DetectionRepo
