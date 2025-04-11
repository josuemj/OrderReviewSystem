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

async def get_all_reviews():
    cursor = db.reviews.find()
    return [dict(r, id=str(r["_id"])) async for r in cursor]

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
