from fastapi import APIRouter, HTTPException
from app.db.client import db
from pydantic import BaseModel
from bson import ObjectId
import bcrypt

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login_user(credentials: LoginRequest):
    user = await db.users.find_one({"email": credentials.email})

    if not user or not bcrypt.checkpw(credentials.password.encode("utf-8"), user["passwordHash"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "orders": user.get("orders", [])  # por si no tiene pedidos aún
    }