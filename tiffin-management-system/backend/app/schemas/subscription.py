from pydantic import BaseModel
from datetime import date


class SubscriptionCreate(BaseModel):
    customer_id: int
    plan_id: int
    start_date: date


class SubscriptionResponse(BaseModel):
    id: int
    customer_id: int
    plan_id: int
    start_date: date
    end_date: date | None
    status: str

    class Config:
        from_attributes = True
