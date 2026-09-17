from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from app.services.subscription_service import create_subscription

router = APIRouter()


@router.post("", response_model=SubscriptionResponse)
def subscribe(data: SubscriptionCreate, db: Session = Depends(get_db)):
    try:
        return create_subscription(
            db=db,
            customer_id=data.customer_id,
            plan_id=data.plan_id,
            start_date=data.start_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
