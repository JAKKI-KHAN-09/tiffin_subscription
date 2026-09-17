from sqlalchemy.orm import Session

from database.models import Subscription, PausePeriod


def pause_subscription(db: Session, subscription_id: int, start_date, end_date, reason):
    subscription = db.get(Subscription, subscription_id)

    if not subscription:
        raise ValueError("Subscription not found")

    if start_date > end_date:
        raise ValueError("Invalid pause dates")

    pause = PausePeriod(
        subscription_id=subscription_id,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
    )

    subscription.status = "PAUSED"
    db.add(pause)
    db.commit()
    db.refresh(pause)

    return pause


def resume_subscription(db: Session, subscription_id: int):
    subscription = db.get(Subscription, subscription_id)

    if not subscription:
        raise ValueError("Subscription not found")

    subscription.status = "ACTIVE"
    db.commit()
    db.refresh(subscription)

    return subscription
