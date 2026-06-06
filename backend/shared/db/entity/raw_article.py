from sqlalchemy import (
    Boolean, Integer, Text, ForeignKey,
    TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from shared.db.entity.base import Base

class RawArticle(Base):
    __tablename__ = "raw_article"

    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    source_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("source.id")
    )

    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    source_name: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str | None] = mapped_column(Text, nullable=False)
    body_text: Mapped[str | None] = mapped_column(Text)
    description_text: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str | None] = mapped_column(Text)
    country: Mapped[str] = mapped_column(Text)
    is_state_affiliated: Mapped[bool] = mapped_column(Boolean, nullable=False)

    published_at: Mapped[str] = mapped_column(TIMESTAMP)
    ingested_at: Mapped[str] = mapped_column(
        TIMESTAMP, server_default="NOW()"
    )
    
    is_processed = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    source = relationship("Source", back_populates="articles")
    processed = relationship("ProcessedArticle", back_populates="raw", uselist=False)
