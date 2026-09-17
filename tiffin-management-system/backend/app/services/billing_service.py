from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from database.models import Subscription
from app.utils.date_utils import get_month_dates, get_service_days
from app.utils.billing_utils import get_paused_service_days


def calculate_bill(db: Session, customer_id: int, billing_month: str):
    year, month = map(int, billing_month.split("-"))

    month_start, month_end = get_month_dates(year, month)

    subscription = (
        db.query(Subscription)
        .filter(Subscription.customer_id == customer_id)
        .filter(Subscription.start_date <= month_end)
        .first()
    )

    if not subscription:
        raise ValueError("No active subscription found")

    service_start = max(subscription.start_date, month_start)
    service_end = month_end

    if subscription.end_date:
        service_end = min(subscription.end_date, month_end)

    if service_start > service_end:
        raise ValueError("No service days in this period")

    service_days = get_service_days(service_start, service_end)
    paused_days = get_paused_service_days(service_days, subscription.pauses)

    scheduled_days = len(service_days)
    paused_count = len(paused_days)
    served_days = scheduled_days - paused_count

    monthly_price = Decimal(str(subscription.plan.monthly_price))

    if scheduled_days == 0:
        raise ValueError("No service days available")

    daily_rate = monthly_price / Decimal(scheduled_days)
    total_amount = daily_rate * Decimal(served_days)

    daily_rate = daily_rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total_amount = total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "customer_id": customer_id,
        "subscription_id": subscription.id,
        "billing_month": billing_month,
        "scheduled_days": scheduled_days,
        "paused_days": paused_count,
        "served_days": served_days,
        "daily_rate": daily_rate,
        "total_amount": total_amount,
    }
