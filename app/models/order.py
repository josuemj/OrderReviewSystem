from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    menuItemId: str
    quantity: int
    price: float

class CreateOrder(BaseModel):
    userId: str
    restaurantId: str
    items: List[OrderItem]
    total: float
