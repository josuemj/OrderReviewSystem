from fastapi import APIRouter, HTTPException, Query
from app.controller import user as crud
from app.schemas.user import UserCreate, UserUpdate, UserOut
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=str)
async def create_user(user: UserCreate):
    return await crud.create_user(user.dict())

@router.get("/", response_model=List[UserOut])
async def get_all_users(page: int = Query(1, ge=1), limit: int = Query(10, le=50)):
    return await crud.get_all_users(page=page, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    user = await crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    updated = await crud.update_user(user_id, user.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o sin cambios")
    return {"message": "Usuario actualizado"}

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    deleted = await crud.delete_user_and_related(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario y sus datos relacionados eliminados"}
