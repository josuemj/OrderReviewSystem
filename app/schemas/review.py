from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    userId: str
    restaurantId: str
    orderId: str
    rating: float
    comment: str

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[float]
    comment: Optional[str]

class ReviewOut(ReviewBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
