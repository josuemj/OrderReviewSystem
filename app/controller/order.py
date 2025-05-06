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

async def get_total_orders():
    result = await db["orders"].count_documents({})
    return result

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

async def update_order_by_id(order_id: str, payload):
    try:
        result = await orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "items": [
                        {
                            "menuItemId": ObjectId(item.menuItemId),
                            "quantity": item.quantity,
                            "price": item.price
                        } for item in payload.items
                    ],
                    "total": payload.total,
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        return result.modified_count == 1
    except Exception as e:
        print("Error al actualizar orden:", e)
        return False

async def get_orders_by_user_and_date(user_id: str, start_date: str, end_date: str):
    start_date_obj = datetime.fromisoformat(start_date.replace("Z", ""))
    end_date_obj = datetime.fromisoformat(end_date.replace("Z", ""))

    pipeline = [
        {
            "$addFields": {
                "createdAtDate": {
                    "$toDate": "$createdAt"
                }
            }
        },
        {
            "$match": {
                "userId": ObjectId(user_id),
                "createdAtDate": {
                    "$gte": start_date_obj,
                    "$lte": end_date_obj
                }
            }
        }
    ]
    orders = await db.orders.aggregate(pipeline).to_list(length=None)
    return fix_objectid(orders)

def fix_objectid(doc):
    if isinstance(doc, list):
        return [fix_objectid(item) for item in doc]
    elif isinstance(doc, dict):
        return {key: fix_objectid(value) for key, value in doc.items()}
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

async def get_orders_with_menu_names_sorted(user_id: str):
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
        },
        {
            "$sort": {
                "total": -1 
            }
        }
    ]

    orders = await db.orders.aggregate(pipeline).to_list(length=None)
    return fix_objectid(orders)  # Usamos el fix para ObjectId

async def get_pending_orders_by_restaurant(restaurant_id: str):
    try:
        restaurant_obj_id = ObjectId(restaurant_id)
    except Exception:
        return []

    query = {
        "restaurantId": restaurant_obj_id,
        "status": {"$ne": "entregado"}
    }

    orders = await db.orders.find(query).to_list(length=25)  # 👈 límite de 25
    return [convert_objectids_recursive(order) for order in orders]

def convert_objectids_recursive(obj):
    if isinstance(obj, dict):
        return {k: convert_objectids_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectids_recursive(i) for i in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj
