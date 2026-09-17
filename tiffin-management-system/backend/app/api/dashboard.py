from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Customer, Subscription

router = APIRouter()


@router.get("")
def dashboard(db: Session = Depends(get_db)):
    total_customers = db.query(Customer).count()
    active_customers = db.query(Subscription).filter(Subscription.status == "ACTIVE").count()
    paused_customers = db.query(Subscription).filter(Subscription.status == "PAUSED").count()

    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "paused_customers": paused_customers,
    }
