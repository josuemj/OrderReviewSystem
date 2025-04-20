from fastapi import APIRouter
from app.controller import order as crud
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.order import CreateOrder
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
async def create_order(order: CreateOrder):
    return await crud.create_order(order)
