from pydantic import BaseModel
from typing import Optional


class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: Optional[str] = None

    class Config:
        from_attributes = True
