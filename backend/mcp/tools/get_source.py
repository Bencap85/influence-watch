from typing import Dict

from shared.db.connect import SessionLocal
from shared.db.entity import Source

def get_source(source_id: int) -> Dict[str, str|int|bool|None]:
    with SessionLocal() as db:
        s = db.query(Source).filter(Source.id == source_id).first()

        if not s:
            return {"error": "not_found"}

        return {
            "source_id": s.id,
            "name": s.name,
            "country_code": s.country_code,
            "is_state_affiliated": s.is_state_affiliated,
            "base_url": s.base_url,
            "description": s.description,
        }
