from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Customer, NotificationOutbox, Subscription

router = APIRouter()


@router.post("/clock")
def generate_clock_outbox(payload: dict | None = None, db: Session = Depends(get_db)):
    clock_date = (payload or {}).get("clock_date") if payload else None
    target_date = date.fromisoformat(clock_date) if clock_date else date.today()

    active_subscriptions = (
        db.query(Subscription)
        .join(Customer)
        .filter(Subscription.status == "ACTIVE")
        .filter(Subscription.start_date <= target_date)
        .all()
    )

    outbox = []
    for subscription in active_subscriptions:
        if subscription.customer is None:
            continue
        if subscription.end_date and subscription.end_date < target_date:
            continue

        if subscription.customer.phone in {"", None}:
            continue

        if subscription.pauses:
            paused = any(
                pause.start_date <= target_date <= pause.end_date for pause in subscription.pauses
            )
            if paused:
                continue

        message = f"Daily delivery reminder for {subscription.customer.name}: plan {subscription.plan.name if subscription.plan else 'standard'} scheduled for {target_date.isoformat()}"
        outbox_item = NotificationOutbox(
            customer_id=subscription.customer_id,
            subscription_id=subscription.id,
            delivery_date=target_date,
            channel="SMS",
            message=message,
            status="queued",
        )
        db.add(outbox_item)
        outbox.append({
            "customer_id": subscription.customer_id,
            "subscription_id": subscription.id,
            "delivery_date": target_date.isoformat(),
            "message": message,
            "status": "queued",
        })

    db.commit()
    return {
        "clock_date": target_date.isoformat(),
        "generated": len(outbox),
        "outbox": outbox,
    }
