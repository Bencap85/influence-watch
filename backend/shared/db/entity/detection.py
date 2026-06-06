from sqlalchemy import (
    Text, ForeignKey,
    TIMESTAMP, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from shared.db.entity.base import Base

class Detection(Base):
    __tablename__ = "detection"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("event.id")
    )

    country_code: Mapped[str] = mapped_column(Text, nullable=False)
    detection_type: Mapped[str] = mapped_column(Text, nullable=False)

    timestamp_detected: Mapped[str] = mapped_column(
        TIMESTAMP, server_default="NOW()"
    )

    evidence = mapped_column(JSON)

    event = relationship("Event", back_populates="detections")