from typing import List, Optional, Any, Dict
from pydantic import BaseModel, RootModel
from datetime import datetime
from uuid import UUID


class EntityItem(RootModel[List[str]]):
    pass

class ProcessedArticleResponse(BaseModel):
    article_id: UUID | str
    title: str
    clean_body_text: Optional[str]
    clean_description_text: Optional[str]
    summary: Optional[str]
    source_name: str
    sentiment_score: Optional[float]
    keyword_list: Optional[List[str]]
    entity_list: Optional[List[EntityItem]]
    country: Optional[str]
    published_at: datetime
    processed_at: Optional[datetime]
    is_state_affiliated: bool

    class Config:
        orm_mode = True
