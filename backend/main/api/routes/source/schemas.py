from pydantic import BaseModel


class SourceResponse(BaseModel):
    id: int
    name: str
    country_code: str
    is_state_affiliated: bool | None
    base_url: str
    description: str | None

    class Config:
        orm_mode = True