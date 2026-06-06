from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from shared.db.entity.base import Base

class EventArticle(Base):
    __tablename__ = "event_article"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("event.id"), primary_key=True
    )

    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("processed_article.article_id"), primary_key=True
    )

    event = relationship("Event", back_populates="articles")
    article = relationship("ProcessedArticle", back_populates="events")
