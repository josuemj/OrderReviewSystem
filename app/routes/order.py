from fastapi import APIRouter, Query
from app.controller import order as crud
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.order import CreateOrder, UpdateItem, UpdateOrderPayload
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
async def create_order(order: CreateOrder):
    return await crud.create_order(order)

@router.get("/user/{user_id}")
async def get_orders_by_user(user_id: str):
    return await crud.get_orders_with_menu_names(user_id)

@router.delete("/{order_id}")
async def delete_order(order_id: str):
    success = await crud.delete_order_by_id(order_id)
    return {"success": success}

@router.put("/{order_id}")
async def update_order(order_id: str, payload: UpdateOrderPayload):
    success = await crud.update_order_by_id(order_id, payload)
    return {"success": success}

@router.get("/by-user-and-date")
async def get_orders_by_user_and_date(
    user_id: str = Query(..., description="ID del usuario"),
    start_date: str = Query(..., description="Fecha de inicio en formato ISO (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Fecha de fin en formato ISO (YYYY-MM-DD)")
):
    return await crud.get_orders_by_user_and_date(user_id, start_date, end_date)