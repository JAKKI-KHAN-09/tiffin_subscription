from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from app.schemas.pause import PauseCreate, PauseResponse
from app.services.pause_service import pause_subscription, resume_subscription

router = APIRouter()


@router.post("/{subscription_id}/pause", response_model=PauseResponse)
def pause(subscription_id: int, data: PauseCreate, db: Session = Depends(get_db)):
    try:
        return pause_subscription(
            db=db,
            subscription_id=subscription_id,
            start_date=data.start_date,
            end_date=data.end_date,
            reason=data.reason,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/{subscription_id}/resume")
def resume(subscription_id: int, db: Session = Depends(get_db)):
    try:
        subscription = resume_subscription(db=db, subscription_id=subscription_id)
        return {
            "message": "Subscription resumed",
            "subscription_id": subscription.id,
            "status": subscription.status,
        }
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
