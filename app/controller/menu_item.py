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
