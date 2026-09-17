from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import create_customer

router = APIRouter()


@router.post("", response_model=CustomerResponse)
def add_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    try:
        return create_customer(
            db=db,
            name=data.name,
            phone=data.phone,
            address=data.address,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/phone/{phone}", response_model=CustomerResponse)
def get_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer
