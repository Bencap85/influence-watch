from sqlalchemy import (
    Integer, Text, Float,
    TIMESTAMP, JSON
)
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from shared.db.entity.base import Base

class Event(Base):
    __tablename__ = "event"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    title: Mapped[str | None] = mapped_column(Text)
    event_summary: Mapped[str | None] = mapped_column(Text)

    centroid_embedding = mapped_column(Vector(1536))

    global_keywords = mapped_column(JSON, default=list)
    global_entities = mapped_column(JSON, default=list)
    global_sentiment: Mapped[float | None] = mapped_column(Float)

    countries = mapped_column(JSON, default=list)
    num_articles: Mapped[int] = mapped_column(Integer, default=1)

    first_seen_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    last_seen_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    articles = relationship("EventArticle", back_populates="event", lazy="raise")
    detections = relationship("Detection", back_populates="event", lazy="raise")


