from sqlalchemy import (
    Text, ForeignKey, Float,
    TIMESTAMP, JSON, text, Boolean
)
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from shared.db.entity.base import Base

class ProcessedArticle(Base):
    __tablename__ = "processed_article"

    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("raw_article.article_id"),
        primary_key=True
    )

    title: Mapped[str | None] = mapped_column(Text)
    clean_body_text: Mapped[str | None] = mapped_column(Text)
    clean_description_text: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    source_name: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(1536))
    sentiment_score: Mapped[float | None] = mapped_column(Float)

    keyword_list = mapped_column(JSON)
    entity_list = mapped_column(JSON)
    country: Mapped[str] = mapped_column(Text)
    is_state_affiliated: Mapped[bool] = mapped_column(Boolean, nullable=False)

    processed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("NOW()")
    )

    published_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    raw = relationship("RawArticle", back_populates="processed")
    events = relationship("EventArticle", back_populates="article")


