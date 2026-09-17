import os
import sys
from datetime import date

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app
from database.database import SessionLocal
from database.models import Customer, Plan, Subscription


def reset_tables(db):
    db.query(Subscription).delete()
    db.query(Customer).delete()
    db.query(Plan).delete()
    db.commit()

client = TestClient(app)


def create_base_subscription(db):
    reset_tables(db)
    customer_a = Customer(name="Alpha", phone="1111111111", address="A")
    customer_b = Customer(name="Beta", phone="2222222222", address="B")
    plan = Plan(name="Lunch Plan", monthly_price=2000, service_type="LUNCH")
    db.add_all([customer_a, customer_b, plan])
    db.commit()
    db.refresh(customer_a)
    db.refresh(customer_b)
    db.refresh(plan)

    subscription = Subscription(
        customer_id=customer_a.id,
        plan_id=plan.id,
        start_date=date(2026, 9, 1),
        status="ACTIVE",
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return customer_a, customer_b, plan, subscription


def test_clock_creates_outbox_entries():
    db = SessionLocal()
    try:
        create_base_subscription(db)
        response = client.post("/api/clock", json={"clock_date": "2026-09-08"})
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["generated"] >= 1
        assert "outbox" in payload
    finally:
        db.close()


def test_subscription_transfer_keeps_plan_and_cycle():
    db = SessionLocal()
    try:
        customer_a, customer_b, _, subscription = create_base_subscription(db)
        response = client.post(
            f"/api/subscriptions/{subscription.id}/transfer",
            json={"new_customer_id": customer_b.id, "effective_date": "2026-09-15"},
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["subscription_id"] == subscription.id
        assert payload["new_customer_id"] == customer_b.id
        assert payload["plan_id"] == subscription.plan_id
        assert payload["status"] == "transferred"
    finally:
        db.close()


def test_customer_import_returns_summary():
    response = client.post(
        "/api/customers/import",
        json={
            "customers": [
                {"name": "A", "phone": "9999999999", "address": "X"},
                {"name": "A Dup", "phone": "9999999999", "address": "X"},
                {"name": "B", "phone": "", "address": "Y"},
                {"name": "C", "phone": "1234", "address": "Z", "start_date": "09/15/2026"},
            ]
        },
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["imported"] >= 1
    assert payload["deduped"] >= 1
    assert payload["rejected"] >= 1
    assert set(payload.keys()) >= {"imported", "deduped", "rejected"}
