import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.client import db

from bson import ObjectId
from datetime import datetime
from models.order import CreateOrder

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
        "status": "en preparación",
        "total": order_data.total,
        "platform": "Stratus",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    result = await db["orders"].insert_one(order_dict)
    return {"message": "Orden creada con éxito", "order_id": str(result.inserted_id)}
