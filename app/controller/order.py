import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.client import db

from bson import ObjectId
from datetime import datetime
from models.order import CreateOrder
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

async def create_order(order_data: CreateOrder):
    order_dict = {
        "userId": ObjectId(order_data.userId),
        "restaurantId": ObjectId(order_data.restaurantId),
        "items": [
            {
                "menuItemId": ObjectId(item.menuItemId),
                "quantity": item.quantity,
                "price": item.price
            }
            for item in order_data.items
        ],
        "status": "pendiente",
        "total": order_data.total,
        "platform": "Stratus",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    result = await db["orders"].insert_one(order_dict)
    return {"message": "Orden creada con éxito", "order_id": str(result.inserted_id)}

orders_collection = db["orders"]

async def get_orders_with_menu_names(user_id: str):
    pipeline = [
        {"$match": {"userId": ObjectId(user_id)}},
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "menu_items",
                "localField": "items.menuItemId",
                "foreignField": "_id",
                "as": "itemDetails"
            }
        },
        {"$unwind": "$itemDetails"},
        {
            "$group": {
                "_id": "$_id",
                "userId": {"$first": "$userId"},
                "restaurantId": {"$first": "$restaurantId"},
                "status": {"$first": "$status"},
                "total": {"$first": "$total"},
                "createdAt": {"$first": "$createdAt"},
                "updatedAt": {"$first": "$updatedAt"},
                "items": {
                    "$push": {
                        "menuItemId": "$items.menuItemId",
                        "quantity": "$items.quantity",
                        "price": "$items.price",
                        "name": "$itemDetails.name"
                    }
                }
            }
        }
    ]

    results = await orders_collection.aggregate(pipeline).to_list(length=None)

    for order in results:
        order["_id"] = str(order["_id"])
        order["userId"] = str(order["userId"])
        order["restaurantId"] = str(order["restaurantId"])
        for item in order["items"]:
            item["menuItemId"] = str(item["menuItemId"])

    return results

async def delete_order_by_id(order_id: str):
    try:
        result = await orders_collection.delete_one({"_id": ObjectId(order_id)})
        return result.deleted_count == 1
    except Exception as e:
        print("Error al eliminar orden:", e)
        return False