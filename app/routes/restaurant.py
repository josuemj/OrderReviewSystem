from fastapi import APIRouter, Query, Body, HTTPException
from app.schemas.restaurant import RestaurantBase
from typing import List
from typing import Optional, Dict
from app.controller import restaurant as crud
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.schemas.restaurant import AddCategoriesRequest, RemoveCategoriesRequest
router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/", response_model=Dict[str, str])
async def create_restaurant(restaurant: RestaurantBase):
    result = await crud.create_restaurant(restaurant.dict())
    if not result:
        raise HTTPException(status_code=400, detail="No se pudo crear el restaurante")
    return {"message": "Restaurante creado exitosamente"}

@router.put("/{restaurant_id}", response_model=Dict[str, str])
async def update_restaurant(restaurant_id: str, restaurant: RestaurantBase):
    updated = await crud.update_restaurant(restaurant_id, restaurant.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado o sin cambios")
    return {"message": "Restaurante actualizado correctamente"}

@router.get("/top-rated")
async def top_rated_restaurants(limit: int = Query(default=10, le=50)):
    return await crud.get_top_rated_restaurants(limit)

@router.get("/avg-rating")
async def avg_rating(id: Optional[str] = Query(None)):
    return await crud.get_average_ratings_by_restaurant(id=id)

@router.get("/")
async def list_all_restaurants():
    return await crud.get_all_restaurants()

@router.post("/categories")
async def add_categories(request: AddCategoriesRequest):
    return await crud.add_categories_restaurant(request)

@router.delete("/categories")
async def remove_categories(request: RemoveCategoriesRequest = Body(...)):
    return await crud.remove_categories_restaurant(request)
