

class BriefResponse:

    detection_id: str
    brief: str

    class Config:
        orm_mode = True
