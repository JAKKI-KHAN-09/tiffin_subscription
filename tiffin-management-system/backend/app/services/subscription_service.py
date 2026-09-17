from sqlalchemy.orm import Session

from database.models import Customer, Plan, Subscription


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
