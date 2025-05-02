from fastapi import APIRouter, Path, Query
from app.controller import menu_item as crud
from fastapi import UploadFile, File, Form
from bson import ObjectId
import gridfs
from fastapi.responses import StreamingResponse
import sys
import os

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])

@router.get("/by-restaurant/{restaurant_id}")
async def get_menu_items_by_restaurant(restaurant_id: str):
    return await crud.get_menu_items_by_restaurant_id(restaurant_id)

@router.get("/top")
async def get_top_menu_items(limit: int = Query(10, description="How many top items to return")):
    return await crud.get_top_menu_items(limit)

@router.get("/all")
async def get_all_menu_items():
    return await crud.get_all_menu_items()

@router.post("/")
async def create_menu_item(
    restaurantId: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...)
):
    return await crud.create_menu_item(
        restaurant_id=restaurantId,  
        name=name,
        description=description,
        price=price,
        image_file=image
    )