from fastapi import APIRouter, Query
from typing import List
from app.controller import restaurant as crud

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

#TODO: CRUD Y DEMAS RUTAS FALTAN

@router.get("/top-rated")
async def top_rated_restaurants(limit: int = Query(default=10, le=50)):
    return await crud.get_top_rated_restaurants(limit)
