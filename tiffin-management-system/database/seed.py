from datetime import date

from database.database import Base, engine, SessionLocal
from database.models import Customer, Plan

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_data():
    plan = Plan(name="Monthly Lunch", monthly_price=3000, service_type="LUNCH")
    customer = Customer(name="Rahul Sharma", phone="9876543210", address="Jaipur, Rajasthan")

    db.add(plan)
    db.add(customer)
    db.commit()

    print("Demo data created")


if __name__ == "__main__":
    seed_data()
    db.close()
