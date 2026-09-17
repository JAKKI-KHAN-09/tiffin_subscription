from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from app.services.billing_service import calculate_bill

router = APIRouter()


@router.get("/{customer_id}")
def get_bill(customer_id: int, month: str, db: Session = Depends(get_db)):
    try:
        bill = calculate_bill(db=db, customer_id=customer_id, billing_month=month)
        return bill
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
