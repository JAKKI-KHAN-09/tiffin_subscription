from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship

from database.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="customer")
    bills = relationship("Bill", back_populates="customer")
    notifications = relationship("NotificationOutbox", back_populates="customer")
    subscription_transfers_sent = relationship(
        "SubscriptionTransfer",
        foreign_keys="SubscriptionTransfer.from_customer_id",
        back_populates="from_customer",
    )
    subscription_transfers_received = relationship(
        "SubscriptionTransfer",
        foreign_keys="SubscriptionTransfer.to_customer_id",
        back_populates="to_customer",
    )


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    monthly_price = Column(Numeric(10, 2), nullable=False)
    service_type = Column(String(50), default="LUNCH")

    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(String(20), default="ACTIVE")

    customer = relationship("Customer", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    pauses = relationship("PausePeriod", back_populates="subscription")
    bills = relationship("Bill", back_populates="subscription")
    notifications = relationship("NotificationOutbox", back_populates="subscription")
    transfers = relationship("SubscriptionTransfer", back_populates="subscription")


class PausePeriod(Base):
    __tablename__ = "pause_periods"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String(255), nullable=True)

    subscription = relationship("Subscription", back_populates="pauses")


class NotificationOutbox(Base):
    __tablename__ = "notification_outbox"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    delivery_date = Column(Date, nullable=False, index=True)
    channel = Column(String(50), default="SMS")
    message = Column(Text, nullable=False)
    status = Column(String(20), default="queued")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="notifications")
    subscription = relationship("Subscription", back_populates="notifications")


class SubscriptionTransfer(Base):
    __tablename__ = "subscription_transfers"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    from_customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    to_customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    effective_date = Column(Date, nullable=False)
    prior_cycle_start = Column(Date, nullable=False)
    prior_cycle_end = Column(Date, nullable=True)
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscription = relationship("Subscription", back_populates="transfers")
    from_customer = relationship(
        "Customer",
        foreign_keys=[from_customer_id],
        back_populates="subscription_transfers_sent",
    )
    to_customer = relationship(
        "Customer",
        foreign_keys=[to_customer_id],
        back_populates="subscription_transfers_received",
    )


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    billing_month = Column(String(7), nullable=False)
    scheduled_days = Column(Integer, nullable=False)
    paused_days = Column(Integer, nullable=False)
    served_days = Column(Integer, nullable=False)
    daily_rate = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    customer = relationship("Customer", back_populates="bills")
    subscription = relationship("Subscription", back_populates="bills")
