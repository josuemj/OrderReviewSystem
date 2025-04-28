from fastapi import APIRouter, Path, Query
from app.controller import menu_item as crud

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])

@router.get("/by-restaurant/{restaurant_id}")
async def get_menu_items_by_restaurant(restaurant_id: str):
    return await crud.get_menu_items_by_restaurant_id(restaurant_id)

@router.get("/top")
async def get_top_menu_items(limit: int = Query(10, description="How many top items to return")):
    return await crud.get_top_menu_items(limit)

