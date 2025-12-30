from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    customer_name: str
    customer_contact: str
    merchant_ref: str

class OrderStatusUpdate(BaseModel):
    new_status: str
    source: str

class OrderResponse(BaseModel):
    id: str
    current_status: str
    updated_at: datetime | None
