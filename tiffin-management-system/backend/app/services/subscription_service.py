from sqlalchemy.orm import Session

from database.models import Customer, Plan, Subscription, SubscriptionTransfer


def create_subscription(db: Session, customer_id: int, plan_id: int, start_date):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise ValueError("Customer not found")

    plan = db.get(Plan, plan_id)
    if not plan:
        raise ValueError("Plan not found")

    subscription = Subscription(
        customer_id=customer_id,
        plan_id=plan_id,
        start_date=start_date,
        status="ACTIVE",
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


def transfer_subscription(db: Session, subscription_id: int, new_customer_id: int, effective_date, reason: str | None = None):
    subscription = db.get(Subscription, subscription_id)
    if not subscription:
        raise ValueError("Subscription not found")

    new_customer = db.get(Customer, new_customer_id)
    if not new_customer:
        raise ValueError("New customer not found")

    if subscription.customer_id == new_customer_id:
        raise ValueError("Customer is already assigned to this subscription")

    old_customer_id = subscription.customer_id
    previous_plan_id = subscription.plan_id
    previous_start = subscription.start_date
    previous_end = subscription.end_date

    subscription.customer_id = new_customer_id
    subscription.status = "transferred"
    if effective_date and effective_date >= subscription.start_date:
        subscription.start_date = effective_date

    transfer = SubscriptionTransfer(
        subscription_id=subscription.id,
        from_customer_id=old_customer_id,
        to_customer_id=new_customer_id,
        effective_date=effective_date,
        prior_cycle_start=previous_start,
        prior_cycle_end=previous_end,
        reason=reason,
    )
    db.add(transfer)
    db.commit()
    db.refresh(subscription)
    db.refresh(transfer)

    return {
        "subscription_id": subscription.id,
        "old_customer_id": old_customer_id,
        "new_customer_id": new_customer_id,
        "plan_id": previous_plan_id,
        "effective_date": effective_date,
        "status": "transferred",
        "transfer_id": transfer.id,
    }
