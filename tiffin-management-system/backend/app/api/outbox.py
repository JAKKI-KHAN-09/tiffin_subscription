from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import NotificationOutbox

router = APIRouter()


@router.get("/outbox")
def list_outbox(db: Session = Depends(get_db)):
    rows = db.query(NotificationOutbox).order_by(NotificationOutbox.delivery_date.desc()).all()
    return [
        {
            "id": row.id,
            "customer_id": row.customer_id,
            "subscription_id": row.subscription_id,
            "delivery_date": row.delivery_date.isoformat(),
            "channel": row.channel,
            "message": row.message,
            "status": row.status,
        }
        for row in rows
    ]
