from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    menuItemId: str
    quantity: int
    price: float

class OrderBase(BaseModel):
    userId: str
    restaurantId: str
    items: List[OrderItem]
    status: str
    total: float

class OrderOut(OrderBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
