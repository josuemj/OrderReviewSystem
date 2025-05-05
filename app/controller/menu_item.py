import sys
import os
from datetime import datetime
from bson import ObjectId
import uuid
from bson import ObjectId
import gridfs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bson import ObjectId
from app.db.client import db
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
fs_bucket = AsyncIOMotorGridFSBucket(db)


def convert_objectid(doc):
    # Convierte los ObjectId a strings
    doc["_id"] = str(doc["_id"])
    if "restaurantId" in doc and isinstance(doc["restaurantId"], ObjectId):
        doc["restaurantId"] = str(doc["restaurantId"])
    return doc

async def get_menu_items_by_restaurant_id(restaurant_id: str):
    try:
        object_id = ObjectId(restaurant_id)
    except Exception:
        return []

    items = await db.menu_items.find({"restaurantId": object_id}).to_list(length=None)
    return [convert_objectid(item) for item in items]

async def get_top_menu_items(limit: int = 10):
    pipeline = [
        {"$unwind": "$items"},
        { 
            "$group": {
                "_id": "$items.menuItemId",
                "total_sale_count": {"$sum": "$items.quantity"},
                "total_sales": {"$sum": {"$multiply": ["$items.quantity", "$items.price"]}}
            }
        },
        {
            "$lookup": {
                "from": "menu_items",
                "localField": "_id",
                "foreignField": "_id",
                "as": "menuItem"
            }
        },
        {"$unwind": "$menuItem"},
        {
            "$lookup": {
                "from": "restaurants",
                "localField": "menuItem.restaurantId",
                "foreignField": "_id",
                "as": "restaurant"
            }
        },
        {"$unwind": "$restaurant"},
        {
            "$project": {
                "_id": 0,
                "menuItem_name": "$menuItem.name",
                "total_sales": 1,
                "restaurant_name": "$restaurant.name",
                "total_sale_count": 1
            }
        },
        {"$sort": {"total_sales": -1}},
        {"$limit": limit}  # 👈 aquí usamos el parámetro dinámico
    ]

    results = await db.orders.aggregate(pipeline).to_list(length=None)
    return results

async def get_all_menu_items():
    items_cursor = db.menu_items.find()
    items = []
    async for item in items_cursor:
        item["_id"] = str(item["_id"])  # convertir _id
        item["restaurantId"] = str(item["restaurantId"])  # convertir restaurantId
        if "image_file_id" in item and isinstance(item["image_file_id"], ObjectId):
            item["image_file_id"] = str(item["image_file_id"])  # convertir image_file_id
        items.append(item)
    return items


async def create_menu_item(restaurant_id, name, description, price, image_file):
    # Leer bytes del archivo
    image_bytes = await image_file.read()

    # Subir imagen a GridFS
    file_id = await fs_bucket.upload_from_stream(
        image_file.filename,
        image_bytes
    )

    # Documento del platillo
    new_item = {
        "restaurantId": ObjectId(restaurant_id),
        "name": name,
        "description": description,
        "price": price,
        "image_file_id": file_id,
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat()
    }

    result = await db.menu_items.insert_one(new_item)
    new_item["_id"] = str(result.inserted_id)
    new_item["restaurantId"] = str(new_item["restaurantId"])
    new_item["image_file_id"] = str(file_id)
    return new_item
