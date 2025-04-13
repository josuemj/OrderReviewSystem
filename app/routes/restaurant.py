from fastapi import APIRouter, Query
from typing import List
from typing import Optional
from app.controller import restaurant as crud

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

#TODO: CRUD Y DEMAS RUTAS FALTAN

@router.get("/top-rated")
async def top_rated_restaurants(limit: int = Query(default=10, le=50)):
    return await crud.get_top_rated_restaurants(limit)

@router.get("/avg-rating")
async def avg_rating(id: Optional[str] = Query(None)):
    return await crud.get_average_ratings_by_restaurant(id=id)