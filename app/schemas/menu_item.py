from pydantic import BaseModel, HttpUrl
from datetime import datetime

class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float
    image: HttpUrl

class MenuItemCreate(MenuItemBase):
    restaurantId: str

class MenuItemOut(MenuItemBase):
    id: str
    restaurantId: str
    createdAt: datetime
    updatedAt: datetime
