from fastapi import FastAPI

from app.api import customers
from app.api import subscriptions
from app.api import pauses
from app.api import billing
from app.api import dashboard

app = FastAPI(
    title="Tiffin Management System",
    description="Subscription and Pro-Rated Billing API",
    version="1.0.0"
)

app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["Subscriptions"])
app.include_router(pauses.router, prefix="/api/pauses", tags=["Pause / Resume"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


@app.get("/")
def root():
    return {
        "message": "Tiffin Management System API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
