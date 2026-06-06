from sqlalchemy import (
    ForeignKey, Float,
    JSON
)
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from shared.db.entity.base import Base

class EventAnalytics(Base):
    __tablename__ = "event_analytics"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("event.id"),
        primary_key=True
    )

    country_embeddings = mapped_column(JSON)
    country_keywords = mapped_column(JSON)
    country_entities = mapped_column(JSON)
    country_sentiment = mapped_column(JSON)

    global_baseline_embedding = mapped_column(Vector(1536))
    global_baseline_keywords = mapped_column(JSON)
    global_baseline_entities = mapped_column(JSON)
    global_baseline_sentiment: Mapped[float | None] = mapped_column(Float)
