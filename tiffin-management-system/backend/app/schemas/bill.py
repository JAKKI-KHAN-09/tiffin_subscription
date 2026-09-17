from pydantic import BaseModel
from decimal import Decimal


class BillResponse(BaseModel):
    customer_id: int
    subscription_id: int
    billing_month: str
    scheduled_days: int
    paused_days: int
    served_days: int
    daily_rate: Decimal
    total_amount: Decimal
