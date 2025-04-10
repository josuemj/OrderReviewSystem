from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    userId: str
    restaurantId: str
    orderId: str
    rating: float
    comment: str

class ReviewOut(ReviewBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
