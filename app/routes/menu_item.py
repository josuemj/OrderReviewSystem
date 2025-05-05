from fastapi import APIRouter, Path, Query, HTTPException
from app.controller import menu_item as crud
from fastapi import UploadFile, File, Form
from bson import ObjectId
import gridfs
from fastapi.responses import StreamingResponse
import sys
import os
from app.db.client import db
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
fs_bucket = AsyncIOMotorGridFSBucket(db)

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])

@router.get('/total')
async def get_total_orders():
    count = await crud.get_total_items()
    return {"total": count}


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
@router.get("/images/{file_id}")
async def get_image(file_id: str):
    try:
        file_id = ObjectId(file_id)
        stream = await fs_bucket.open_download_stream(file_id)
        return StreamingResponse(stream, media_type="image/jpeg")
    except Exception:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")