import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bson import ObjectId
from app.db.client import db

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
        item["_id"] = str(item["_id"])  # convertir ObjectId a string
        item["restaurantId"] = str(item["restaurantId"])  # si también es ObjectId
        items.append(item)
    return items
