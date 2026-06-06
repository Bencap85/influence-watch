import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Dict

class DetectionResponse(BaseModel):
    id: uuid.UUID
    event_id: uuid.UUID

    country_code: str
    detection_type: str

    timestamp_detected: datetime

    evidence: Dict

    event_name: str | None

    class Config:
        orm_mode = True
