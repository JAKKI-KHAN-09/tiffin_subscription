from pydantic import BaseModel
from datetime import date


class SubscriptionCreate(BaseModel):
    customer_id: int
    plan_id: int
    start_date: date


class SubscriptionTransferRequest(BaseModel):
    new_customer_id: int
    effective_date: date
    reason: str | None = None


class SubscriptionTransferResponse(BaseModel):
    subscription_id: int
    old_customer_id: int
    new_customer_id: int
    plan_id: int
    effective_date: date
    status: str
    transfer_id: int


class SubscriptionResponse(BaseModel):
    id: int
    customer_id: int
    plan_id: int
    start_date: date
    end_date: date | None
    status: str

    class Config:
        from_attributes = True
