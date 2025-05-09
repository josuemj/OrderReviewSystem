import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.client import db
from bson import ObjectId
from datetime import datetime
from typing import Optional
from fastapi import Query

async def create_restaurant(data):
    data["createdAt"] = datetime.utcnow()
    data["updatedAt"] = datetime.utcnow()
    result = await db.restaurants.insert_one(data)
    return str(result.inserted_id)

async def update_restaurant(restaurant_id, data):
    data["updatedAt"] = datetime.utcnow()
    result = await db.restaurants.update_one(
        {"_id": ObjectId(restaurant_id)},
        {"$set": data}
    )
    return result.modified_count

async def get_restaurants_by_category(category: str):
    docs = await db.restaurants.find({"categories": category}).to_list(length=None)

    cleaned_docs = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # o usa doc.pop("_id", None) si no necesitas el ID
        cleaned_docs.append(doc)

    return cleaned_docs

async def get_all_categories():
    return await db.restaurants.distinct("categories")

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
                "restaurantId": { "$toString": "$restaurant._id" }  
            }
        }
    ]

    return [r async for r in db.reviews.aggregate(pipeline)]

async def get_average_ratings_by_restaurant(id: Optional[str] = Query(None)):
    pipeline = []

    if id:
        try:
            restaurant_oid = ObjectId(id)
            pipeline.append({
                "$match": {"restaurantId": restaurant_oid}
            })
        except Exception:
            return []  

    pipeline.extend([
        {
            "$group": {
                "_id": "$restaurantId",
                "averageRating": {"$avg": "$rating"},
                "totalReviews": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "restaurants",
                "localField": "_id",
                "foreignField": "_id",
                "as": "restaurant"
            }
        },
        {"$unwind": "$restaurant"},
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "name": "$restaurant.name",
                "averageRating": 1,
                "totalReviews": 1
            }
        }
    ])

    result = await db.reviews.aggregate(pipeline).to_list(None)
    return result

async def get_all_restaurants():
    restaurants = await db.restaurants.find().to_list(length=None)
    for r in restaurants:
        r["_id"] = str(r["_id"])
    return restaurants

async def add_categories_restaurant(request):
    restaurant_id = request.restaurant_id
    categories_to_add = request.categories

    # Make sure the ID is valid
    if not ObjectId.is_valid(restaurant_id):
        return {"error": "Invalid restaurant ID"}

    result = await db.restaurants.update_one(
        {"_id": ObjectId(restaurant_id)},
        {
            "$addToSet": {
                "categories": { "$each": categories_to_add }
            }
        }
    )

    if result.modified_count:
        return {"message": "Categories added successfully"}
    else:
        return {"message": "No changes made (maybe categories already existed)"}

async def remove_categories_restaurant(request):
    restaurant_id = request.restaurant_id
    categories_to_remove = request.categories

    if not ObjectId.is_valid(restaurant_id):
        return {"error": "Invalid restaurant ID"}

    result = await db.restaurants.update_one(
        {"_id": ObjectId(restaurant_id)},
        {
            "$pull": {
                "categories": { "$in": categories_to_remove }
            }
        }
    )

    if result.modified_count:
        return {"message": "Categories removed successfully"}
    else:
        return {"message": "No changes made (maybe categories were not found)"}

