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
from typing import List


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

@router.delete("/{menu_item_id}")
async def delete_menu_item(menu_item_id: str):
    success = await crud.delete_menu_item(menu_item_id)
    if success:
        return {"message": "Platillo eliminado correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Platillo no encontrado o error al eliminar")

@router.post("/bulk-create")
async def bulk_create_menu_items(
    restaurantId: str = Form(...),
    names: List[str] = Form(...),
    descriptions: List[str] = Form(...),
    prices: List[float] = Form(...),
    images: List[UploadFile] = File(...)
):
    if not (len(names) == len(descriptions) == len(prices) == len(images)):
        raise HTTPException(status_code=400, detail="Todos los campos deben tener el mismo número de elementos")

    return await crud.bulk_create_menu_items(restaurantId, names, descriptions, prices, images)

@router.put("/{menu_item_id}")
async def update_menu_item(
    menu_item_id: str,
    restaurantId: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(None)  # imagen opcional
):
    print("✅ Llamada recibida para actualizar:", menu_item_id)

    updated = await crud.update_menu_item(
        menu_item_id=menu_item_id,
        restaurant_id=restaurantId,
        name=name,
        description=description,
        price=price,
        image_file=image
    )
    if updated:
        return {"message": "Platillo actualizado correctamente"}
    else:
        raise HTTPException(status_code=404, detail="Error al actualizar platillo")


@router.get("/images/{file_id}")
async def get_image(file_id: str):
    try:
        file_id = ObjectId(file_id)
        stream = await fs_bucket.open_download_stream(file_id)
        return StreamingResponse(stream, media_type="image/jpeg")
    except Exception:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")