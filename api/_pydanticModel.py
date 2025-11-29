from pydantic import BaseModel


class KPIRequest(BaseModel):
    start: str
    end: str
    season: str
    field_stage: str
