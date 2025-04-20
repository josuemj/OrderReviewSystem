from fastapi import APIRouter, HTTPException
from app.db.client import db
from pydantic import BaseModel, EmailStr
from bson import ObjectId
import bcrypt
from datetime import datetime, timezone

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

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

@router.post("/register")
async def register_user(data: RegisterRequest):
    # Verifica si el usuario ya existe
    existing_user = await db.users.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Hashing de contraseña
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), salt).decode("utf-8")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    new_user = {
        "name": data.name,
        "email": data.email,
        "passwordHash": hashed_password,
        "orders": [],
        "createdAt": now,
        "updatedAt": now
    }

    result = await db.users.insert_one(new_user)

    return {
        "message": "Usuario registrado exitosamente",
        "id": str(result.inserted_id),
        "email": data.email,
        "name": data.name
    }
