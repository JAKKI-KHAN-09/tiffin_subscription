from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionTransferRequest, SubscriptionTransferResponse
from app.services.subscription_service import create_subscription, transfer_subscription

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


@router.post("/{subscription_id}/transfer", response_model=SubscriptionTransferResponse)
def transfer_subscription_route(subscription_id: int, data: SubscriptionTransferRequest, db: Session = Depends(get_db)):
    try:
        return transfer_subscription(
            db=db,
            subscription_id=subscription_id,
            new_customer_id=data.new_customer_id,
            effective_date=data.effective_date,
            reason=data.reason,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
