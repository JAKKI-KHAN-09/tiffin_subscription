from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Customer, Plan, Subscription
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import create_customer

router = APIRouter()


def _clean_phone(raw_value):
    if raw_value is None:
        return ""
    digits = "".join(ch for ch in str(raw_value) if ch.isdigit())
    return digits


def _normalize_date(value):
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if hasattr(value, "isoformat"):
        return value
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    return None


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


@router.post("/import")
def import_customers(payload: dict, db: Session = Depends(get_db)):
    customers = payload.get("customers", []) if isinstance(payload, dict) else []
    imported_count = 0
    deduped_count = 0
    rejected_count = 0
    seen_phones = set()
    default_plan = db.query(Plan).first()

    for item in customers:
        if not isinstance(item, dict):
            rejected_count += 1
            continue

        raw_name = (item.get("name") or "").strip()
        raw_phone = _clean_phone(item.get("phone"))
        address = (item.get("address") or "").strip()
        if not raw_name or not raw_phone:
            rejected_count += 1
            continue

        normalized_phone = raw_phone
        if normalized_phone in seen_phones or db.query(Customer).filter(Customer.phone == normalized_phone).first():
            deduped_count += 1
            continue

        seen_phones.add(normalized_phone)

        customer = Customer(name=raw_name, phone=normalized_phone, address=address or None)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        imported_count += 1

        subscription_start = _normalize_date(item.get("start_date"))
        if subscription_start and default_plan:
            existing = db.query(Subscription).filter(Subscription.customer_id == customer.id).first()
            if not existing:
                sub = Subscription(
                    customer_id=customer.id,
                    plan_id=default_plan.id,
                    start_date=subscription_start,
                    status="ACTIVE",
                )
                db.add(sub)
                db.commit()

    return {
        "imported": imported_count,
        "deduped": deduped_count,
        "rejected": rejected_count,
    }


@router.get("/phone/{phone}", response_model=CustomerResponse)
def get_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == phone).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer
