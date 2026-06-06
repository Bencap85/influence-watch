from sqlalchemy import (
    Boolean, Integer, Text
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from shared.db.entity.base import Base

class Source(Base):
    __tablename__ = "source"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    country_code: Mapped[str] = mapped_column(Text, nullable=False)
    is_state_affiliated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    base_url: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)

    articles = relationship("RawArticle", back_populates="source")
