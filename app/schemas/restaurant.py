from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    address: str
    city: str
    coordinates: dict  # o puedes usar: Dict[str, float]

class RestaurantBase(BaseModel):
    name: str
    location: Location
    categories: List[str]

class RestaurantOut(RestaurantBase):
    id: str
    menu: Optional[List[str]] = []
    createdAt: datetime
    updatedAt: datetime
    
class AddCategoriesRequest(BaseModel):
    restaurant_id: str
    categories: List[str]
    
class RemoveCategoriesRequest(BaseModel):
    restaurant_id: str
    categories: List[str]
