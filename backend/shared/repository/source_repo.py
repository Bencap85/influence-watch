from typing import List

from shared.db.entity import Source
from sqlalchemy.orm import Session

class SourceRepo():
    
    def get_all(self, db: Session) -> List[Source]:
        return db.query(Source).all()
    
    def get_by_id(self, source_id: int, db: Session) -> Source | None:
        return db.query(Source).filter(Source.id == source_id).first()
    
    def save(self, db: Session, source: Source) -> Source:
        db.add(source)
        db.commit()
        return source