import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.client import db
from bson import ObjectId
from datetime import datetime

#TODO: CRUD Y DEMAS FUNCIONES FALTAN

async def get_top_rated_restaurants(limit: int = 10):
    pipeline = [
        {
            "$group": {
                "_id": "$restaurantId",
                "averageRating": { "$avg": "$rating" },
                "reviewCount": { "$sum": 1 }
            }
        },
        {
            "$sort": { "averageRating": -1 }
        },
        {
            "$limit": limit
        },
        {
            "$lookup": {
                "from": "restaurants",
                "localField": "_id",
                "foreignField": "_id",
                "as": "restaurant"
            }
        },
        {
            "$unwind": "$restaurant"
        },
        {
            "$project": {
                "_id": 0,
                "id": { "$toString": "$_id" },
                "averageRating": 1,
                "reviewCount": 1,
                "name": "$restaurant.name",
                "location": "$restaurant.location",
                "categories": "$restaurant.categories",
                "restaurantId": { "$toString": "$restaurant._id" }  # <- este era el problema real
            }
        }
    ]

    return [r async for r in db.reviews.aggregate(pipeline)]
