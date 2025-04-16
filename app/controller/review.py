import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.client import db
from bson import ObjectId
from datetime import datetime

async def create_review(data):
    now = datetime.utcnow()
    data["createdAt"] = now
    data["updatedAt"] = now
    result = await db.reviews.insert_one(data)
    return str(result.inserted_id)

async def get_all_reviews(skip: int = 0, limit: int = 10):
    cursor = db.reviews.find().skip(skip).limit(limit)
    results = []

    async for r in cursor:
        r["id"] = str(r["_id"])
        r["_id"] = str(r["_id"])
        if "restaurantId" in r:
            r["restaurantId"] = str(r["restaurantId"])
        if "orderId" in r:
            r["orderId"] = str(r["orderId"])
        if "userId" in r:
            r["userId"] = str(r["userId"])
        results.append(r)

    return results

async def get_review_by_id(review_id):
    review = await db.reviews.find_one({"_id": ObjectId(review_id)})
    if review:
        review["id"] = str(review["_id"])
        return review
    return None

async def update_review(review_id, data):
    data["updatedAt"] = datetime.utcnow()
    result = await db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": data})
    return result.modified_count

async def delete_review(review_id):
    result = await db.reviews.delete_one({"_id": ObjectId(review_id)})
    return result.deleted_count

async def get_reviews_by_relevance(limit: int = 10, restaurant_id: str = None, min_rating: float = None):
    query = {}

    if restaurant_id:
        query["restaurantId"] = restaurant_id

    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}

    cursor = db.reviews.find(query).sort([
        ("rating", -1),
        ("createdAt", -1)
    ]).limit(limit)

    return [dict(r, id=str(r["_id"])) async for r in cursor]
