

import uuid
from datetime import datetime
from pydantic import RootModel, BaseModel
from typing import List, Optional, Dict, Any

class EntityItem(RootModel[Dict[str, Any]]):
    pass

class EventResponse(BaseModel):
    id: uuid.UUID
    title: str | None
    event_summary: str | None

    global_keywords: Optional[List[str]] 
    global_entities: Optional[List[EntityItem]]
    global_sentiment: float | None

    countries: Optional[List[str]]
    num_articles: int

    first_seen_at: datetime
    last_seen_at: datetime

    class Config:
        orm_mode = True
    