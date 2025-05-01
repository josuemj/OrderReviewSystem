from app.db.client import db
from bson import ObjectId
from datetime import datetime
import bcrypt

async def create_user(data):
    now = datetime.utcnow()
    data["createdAt"] = now
    data["updatedAt"] = now
    result = await db.users.insert_one(data)
    return str(result.inserted_id)

async def get_all_users(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    cursor = db.users.find().skip(skip).limit(limit)
    results = []
    async for user in cursor:
        user["id"] = str(user["_id"])
        user.pop("_id", None)
        results.append(user)
    return results


async def get_user_by_id(user_id):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        return user
    return None

async def update_user(user_id, data):
    data["updatedAt"] = datetime.utcnow()

    # Procesar nueva contraseña si se incluye
    if "password" in data and data["password"]:
        hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        data["passwordHash"] = hashed
        del data["password"]

    result = await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    return result.modified_count

async def delete_user_and_related(user_id):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return False

    user_deleted = await db.users.delete_one({"_id": oid})
    await db.orders.delete_many({"userId": oid})
    await db.reviews.delete_many({"userId": oid})
    
    return user_deleted.deleted_count > 0
