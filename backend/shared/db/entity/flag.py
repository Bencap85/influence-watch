from sqlalchemy import Boolean, Column, String

from shared.db.entity.base import Base

class Flag(Base):
    __tablename__ = "flag"

    name = Column(String, primary_key=True)
    completed = Column(Boolean, nullable=False)
