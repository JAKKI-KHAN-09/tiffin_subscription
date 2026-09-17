from pydantic import BaseModel
from datetime import date
from typing import Optional


class PauseCreate(BaseModel):
    start_date: date
    end_date: date
    reason: Optional[str] = None


class PauseResponse(BaseModel):
    id: int
    subscription_id: int
    start_date: date
    end_date: date
    reason: Optional[str]

    class Config:
        from_attributes = True
