from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import customers
from app.api import subscriptions
from app.api import pauses
from app.api import billing
from app.api import dashboard
from app.api import clock
from app.api import outbox
from database import models  # noqa: F401
from database.database import Base, engine

app = FastAPI(
    title="Tiffin Management System",
    description="Subscription and Pro-Rated Billing API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    from database import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["Subscriptions"])
app.include_router(pauses.router, prefix="/api/pauses", tags=["Pause / Resume"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(clock.router, prefix="/api", tags=["Clock"])
app.include_router(outbox.router, prefix="/api", tags=["Outbox"])


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
