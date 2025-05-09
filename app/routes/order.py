from fastapi import APIRouter, Body, HTTPException, Query
from app.controller import order as crud
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.order import CreateOrder, UpdateItem, UpdateOrderPayload
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.put("/update-by-restaurant")
async def update_orders_by_restaurant(data: dict = Body(...)): 
    restaurant_id = data.get("restaurantId")
    updates = data.get("updates", [])

    if not restaurant_id or not updates:
        raise HTTPException(status_code=400, detail="Faltan datos")

    updated = await crud.bulk_update_orders_by_restaurant(restaurant_id, updates)
    return {"updated_count": updated}

@router.post("/")
async def create_order(order: CreateOrder):
    return await crud.create_order(order)

@router.get('/total')
async def get_total_orders():
    count = await crud.get_total_orders()
    return {"total": count}

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

@router.get("/usersortorders/{user_id}")
async def get_orders_by_user_sorted(user_id: str):
    return await crud.get_orders_with_menu_names_sorted(user_id)

@router.get("/pending/{restaurant_id}")
async def get_pending_orders(restaurant_id: str):
    return await crud.get_pending_orders_by_restaurant(restaurant_id)


