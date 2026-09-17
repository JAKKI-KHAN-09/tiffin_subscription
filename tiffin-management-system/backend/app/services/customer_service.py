from sqlalchemy.orm import Session

from database.models import Customer


def create_customer(db: Session, name: str, phone: str, address: str | None):
    existing = db.query(Customer).filter(Customer.phone == phone).first()

    if existing:
        raise ValueError("Customer with this phone already exists")

    customer = Customer(name=name, phone=phone, address=address)
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer
