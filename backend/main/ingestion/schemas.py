from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RSSArticle(BaseModel):
    title: str
    description: Optional[str]
    url: str
    source_name: str
    published_at: Optional[datetime]
    content: Optional[str]
    source_id: Optional[int]
    country_code: Optional[str]
    is_state_affiliated: bool
